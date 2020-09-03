# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import pytest

from trezorlib import tools
from trezorlib.cardano import (
    NETWORK_IDS,
    PROTOCOL_MAGICS,
    create_address_parameters,
    get_address,
)
from trezorlib.messages import CardanoAddressType


@pytest.mark.altcoin
@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
@pytest.mark.parametrize(
    "path,protocol_magic,expected_address",
    [
        # mainnet
        (
            "m/44'/1815'/0'/0/0",
            PROTOCOL_MAGICS["mainnet"],
            "Ae2tdPwUPEZ5YUb8sM3eS8JqKgrRLzhiu71crfuH2MFtqaYr5ACNRdsswsZ",
        ),
        (
            "m/44'/1815'/0'/0/1",
            PROTOCOL_MAGICS["mainnet"],
            "Ae2tdPwUPEZJb8r1VZxweSwHDTYtqeYqF39rZmVbrNK62JHd4Wd7Ytsc8eG",
        ),
        (
            "m/44'/1815'/0'/0/2",
            PROTOCOL_MAGICS["mainnet"],
            "Ae2tdPwUPEZFm6Y7aPZGKMyMAK16yA5pWWKU9g73ncUQNZsAjzjhszenCsq",
        ),
        # testnet
        # data generated by code under test
        (
            "m/44'/1815'/0'/0/0",
            PROTOCOL_MAGICS["testnet"],
            "2657WMsDfac5F3zbgs9BwNWx3dhGAJERkAL93gPa68NJ2i8mbCHm2pLUHWSj8Mfea",
        ),
        (
            "m/44'/1815'/0'/0/1",
            PROTOCOL_MAGICS["testnet"],
            "2657WMsDfac6ezKWszxLFqJjSUgpg9NgxKc1koqi24sVpRaPhiwMaExk4useKn5HA",
        ),
        (
            "m/44'/1815'/0'/0/2",
            PROTOCOL_MAGICS["testnet"],
            "2657WMsDfac7hr1ioJGr6g7r6JRx4r1My8Rj91tcPTeVjJDpfBYKURrPG2zVLx2Sq",
        ),
    ],
)
def test_cardano_get_address(client, path, protocol_magic, expected_address):
    address = get_address(
        client,
        address_parameters=create_address_parameters(
            address_type=CardanoAddressType.BYRON, address_n=tools.parse_path(path),
        ),
        protocol_magic=protocol_magic,
        network_id=NETWORK_IDS["mainnet"],
    )
    assert address == expected_address


@pytest.mark.altcoin
@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
@pytest.mark.parametrize(
    "path, staking_path, network_id, expected_address",
    [
        # data generated with code under test
        (
            "m/1852'/1815'/4'/0/0",
            "m/1852'/1815'/4'/2/0",
            NETWORK_IDS["mainnet"],
            "addr1q8v42wjda8r6mpfj40d36znlgfdcqp7jtj03ah8skh6u8wnrqua2vw243tmjfjt0h5wsru6appuz8c0pfd75ur7myyeqsx9990",
        ),
        (
            "m/1852'/1815'/4'/0/0",
            "m/1852'/1815'/4'/2/0",
            NETWORK_IDS["testnet"],
            "addr_test1qrv42wjda8r6mpfj40d36znlgfdcqp7jtj03ah8skh6u8wnrqua2vw243tmjfjt0h5wsru6appuz8c0pfd75ur7myyeqnsc9fs",
        ),
    ],
)
def test_cardano_get_base_address(
    client, path, staking_path, network_id, expected_address
):
    address = get_address(
        client,
        address_parameters=create_address_parameters(
            address_type=CardanoAddressType.BASE,
            address_n=tools.parse_path(path),
            address_n_staking=tools.parse_path(staking_path),
        ),
        protocol_magic=PROTOCOL_MAGICS["mainnet"],
        network_id=network_id,
    )
    assert address == expected_address


@pytest.mark.altcoin
@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
@pytest.mark.parametrize(
    "path, staking_key_hash, network_id, expected_address",
    [
        # data generated with code under test
        (
            "m/1852'/1815'/4'/0/0",
            "1bc428e4720702ebd5dab4fb175324c192dc9bb76cc5da956e3c8dff",
            NETWORK_IDS["mainnet"],
            "addr1q8v42wjda8r6mpfj40d36znlgfdcqp7jtj03ah8skh6u8wsmcs5wgus8qt4atk45lvt4xfxpjtwfhdmvchdf2m3u3hlsydc62k",
        ),
        (
            "m/1852'/1815'/4'/0/0",
            "1bc428e4720702ebd5dab4fb175324c192dc9bb76cc5da956e3c8dff",
            NETWORK_IDS["testnet"],
            "addr_test1qrv42wjda8r6mpfj40d36znlgfdcqp7jtj03ah8skh6u8wsmcs5wgus8qt4atk45lvt4xfxpjtwfhdmvchdf2m3u3hls8m96xf",
        ),
        # staking key hash not owned - derived with "all all..." mnenomnic, data generated with code under test
        (
            "m/1852'/1815'/4'/0/0",
            "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
            NETWORK_IDS["mainnet"],
            "addr1q8v42wjda8r6mpfj40d36znlgfdcqp7jtj03ah8skh6u8wsj922xhxkn6twlq2wn4q50q352annk3903tj00h45mgfms06skxl",
        ),
        (
            "m/1852'/1815'/0'/0/0",
            "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
            NETWORK_IDS["testnet"],
            "addr_test1qzq0nckg3ekgzuqg7w5p9mvgnd9ym28qh5grlph8xd2z92sj922xhxkn6twlq2wn4q50q352annk3903tj00h45mgfmsu8d9w5",
        ),
        (
            "m/1852'/1815'/4'/0/0",
            "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
            NETWORK_IDS["testnet"],
            "addr_test1qrv42wjda8r6mpfj40d36znlgfdcqp7jtj03ah8skh6u8wsj922xhxkn6twlq2wn4q50q352annk3903tj00h45mgfmsvvdk2q",
        ),
    ],
)
def test_cardano_get_base_address_with_staking_key_hash(
    client, path, staking_key_hash, network_id, expected_address
):
    # data form shelley test vectors
    address = get_address(
        client,
        address_parameters=create_address_parameters(
            address_type=CardanoAddressType.BASE,
            address_n=tools.parse_path(path),
            staking_key_hash=bytes.fromhex(staking_key_hash),
        ),
        protocol_magic=PROTOCOL_MAGICS["mainnet"],
        network_id=network_id,
    )
    assert address == expected_address


@pytest.mark.altcoin
@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
@pytest.mark.parametrize(
    "path, network_id, expected_address",
    [
        # data generated with code under test
        (
            "m/1852'/1815'/0'/0/0",
            NETWORK_IDS["mainnet"],
            "addr1vxq0nckg3ekgzuqg7w5p9mvgnd9ym28qh5grlph8xd2z92su77c6m",
        ),
        (
            "m/1852'/1815'/0'/0/0",
            NETWORK_IDS["testnet"],
            "addr_test1vzq0nckg3ekgzuqg7w5p9mvgnd9ym28qh5grlph8xd2z92s8k2y47",
        ),
    ],
)
def test_cardano_get_enterprise_address(client, path, network_id, expected_address):
    address = get_address(
        client,
        address_parameters=create_address_parameters(
            address_type=CardanoAddressType.ENTERPRISE,
            address_n=tools.parse_path(path),
        ),
        protocol_magic=PROTOCOL_MAGICS["mainnet"],
        network_id=network_id,
    )
    assert address == expected_address


@pytest.mark.altcoin
@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
@pytest.mark.parametrize(
    "path, block_index, tx_index, certificate_index, network_id, expected_address",
    [
        # data generated with code under test
        (
            "m/1852'/1815'/0'/0/0",
            1,
            2,
            3,
            NETWORK_IDS["mainnet"],
            "addr1gxq0nckg3ekgzuqg7w5p9mvgnd9ym28qh5grlph8xd2z92spqgpsl97q83",
        ),
        (
            "m/1852'/1815'/0'/0/0",
            24157,
            177,
            42,
            NETWORK_IDS["testnet"],
            "addr_test1gzq0nckg3ekgzuqg7w5p9mvgnd9ym28qh5grlph8xd2z925ph3wczvf2ag2x9t",
        ),
    ],
)
def test_cardano_get_pointer_address(
    client,
    path,
    block_index,
    tx_index,
    certificate_index,
    network_id,
    expected_address,
):
    address = get_address(
        client,
        address_parameters=create_address_parameters(
            address_type=CardanoAddressType.POINTER,
            address_n=tools.parse_path(path),
            block_index=block_index,
            tx_index=tx_index,
            certificate_index=certificate_index,
        ),
        protocol_magic=PROTOCOL_MAGICS["mainnet"],
        network_id=network_id,
    )
    assert address == expected_address


@pytest.mark.altcoin
@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
@pytest.mark.parametrize(
    "path, network_id, expected_address",
    [
        # data generated with code under test
        (
            "m/1852'/1815'/0'/2/0",
            NETWORK_IDS["mainnet"],
            "stake1uyfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yacalmqha",
        ),
        (
            "m/1852'/1815'/0'/2/0",
            NETWORK_IDS["testnet"],
            "stake_test1uqfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yac643znq",
        ),
    ],
)
def test_cardano_get_reward_address(client, path, network_id, expected_address):
    address = get_address(
        client,
        address_parameters=create_address_parameters(
            address_type=CardanoAddressType.REWARD, address_n=tools.parse_path(path),
        ),
        protocol_magic=PROTOCOL_MAGICS["mainnet"],
        network_id=network_id,
    )
    assert address == expected_address