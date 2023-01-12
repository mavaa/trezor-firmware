from typing import TYPE_CHECKING

from . import text_r

if TYPE_CHECKING:
    from typing import Awaitable
    from trezor.wire import Context

    from trezor.messages import ChangeWipeCode, Success


async def change_wipe_code(ctx: Context, msg: ChangeWipeCode) -> Success:
    from storage.device import is_initialized
    from trezor.wire import NotInitialized
    from trezor.ui.layouts import show_success
    from trezor.messages import Success
    from trezor import config
    from apps.common.request_pin import (
        error_pin_invalid,
        request_pin_and_sd_salt,
    )

    if not is_initialized():
        raise NotInitialized("Device is not initialized")

    # Confirm that user wants to set or remove the wipe code.
    has_wipe_code = config.has_wipe_code()
    await _require_confirm_action(ctx, msg, has_wipe_code)

    # Get the unlocking PIN.
    pin, salt = await request_pin_and_sd_salt(ctx, "Enter PIN")

    if not msg.remove:
        # Pre-check the entered PIN.
        if config.has_pin() and not config.check_pin(pin, salt):
            await error_pin_invalid(ctx)

        # Get new wipe code.
        wipe_code = await _request_wipe_code_confirm(ctx, pin)
    else:
        wipe_code = ""

    # Write into storage.
    if not config.change_wipe_code(pin, salt, wipe_code):
        await error_pin_invalid(ctx)

    if wipe_code:
        if has_wipe_code:
            msg_screen = "Wipe code changed."
            msg_wire = "Wipe code changed"
        else:
            msg_screen = "Wipe code enabled."
            msg_wire = "Wipe code set"
    else:
        msg_screen = "Wipe code disabled."
        msg_wire = "Wipe code removed"

    await show_success(ctx, "success_wipe_code", msg_screen)
    return Success(message=msg_wire)


def _require_confirm_action(
    ctx: Context, msg: ChangeWipeCode, has_wipe_code: bool
) -> Awaitable[None]:
    from trezor.wire import ProcessError
    from trezor.ui.layouts import confirm_pin_action, confirm_set_new_pin

    title = "Wipe code settings"

    if msg.remove and has_wipe_code:
        return confirm_pin_action(
            ctx,
            "disable_wipe_code",
            title,
            "disable wipe code protection?",
        )

    if not msg.remove and has_wipe_code:
        return confirm_pin_action(
            ctx,
            "change_wipe_code",
            title,
            "change the wipe code?",
        )

    if not msg.remove and not has_wipe_code:
        return confirm_set_new_pin(
            ctx,
            "set_wipe_code",
            title,
            "enable wipe code?",
            [
                "Wipe code can be used to erase all data from this device.",
            ],
        )

    # Removing non-existing wipe code.
    raise ProcessError("Wipe code protection is already disabled")


async def _request_wipe_code_confirm(ctx: Context, pin: str) -> str:
    from trezor.ui.layouts import show_popup
    from apps.common.request_pin import request_pin

    while True:
        code1 = await request_pin(ctx, "Enter new wipe code")
        if code1 == pin:
            # _wipe_code_invalid
            await show_popup(
                "Invalid wipe code",
                text_r(
                    "The wipe code must be\ndifferent from your PIN.\n\nPlease try again."
                ),
            )
            continue

        code2 = await request_pin(ctx, "Re-enter wipe code")
        if code1 == code2:
            return code1
        # _wipe_code_mismatch
        await show_popup(
            "Code mismatch",
            text_r("The wipe codes you\nentered do not match.\n\nPlease try again."),
        )
