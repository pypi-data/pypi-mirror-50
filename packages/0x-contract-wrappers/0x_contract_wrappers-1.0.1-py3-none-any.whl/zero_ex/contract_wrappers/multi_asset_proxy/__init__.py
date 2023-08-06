"""Generated wrapper for MultiAssetProxy Solidity contract."""

# pylint: disable=too-many-arguments

import json
from typing import (  # pylint: disable=unused-import
    Any,
    List,
    Optional,
    Tuple,
    Union,
)

from eth_utils import to_checksum_address
from mypy_extensions import TypedDict  # pylint: disable=unused-import
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import ContractFunction
from web3.datastructures import AttributeDict
from web3.providers.base import BaseProvider

from zero_ex.contract_wrappers.bases import ContractMethod, Validator
from zero_ex.contract_wrappers.tx_params import TxParams


# Try to import a custom validator class definition; if there isn't one,
# declare one that we can instantiate for the default argument to the
# constructor for MultiAssetProxy below.
try:
    # both mypy and pylint complain about what we're doing here, but this
    # works just fine, so their messages have been disabled here.
    from . import (  # type: ignore # pylint: disable=import-self
        MultiAssetProxyValidator,
    )
except ImportError:

    class MultiAssetProxyValidator(  # type: ignore
        Validator
    ):
        """No-op input validator."""


class AssetProxiesMethod(ContractMethod):
    """Various interfaces to the assetProxies method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def validate_and_normalize_inputs(self, index_0: bytes):
        """Validate the inputs to the assetProxies method."""
        self.validator.assert_valid(
            method_name="assetProxies",
            parameter_name="index_0",
            argument_value=index_0,
        )
        return index_0

    def call(
        self, index_0: bytes, tx_params: Optional[TxParams] = None
    ) -> str:
        """Execute underlying contract method via eth_call.

        :param tx_params: transaction parameters

        """
        (index_0) = self.validate_and_normalize_inputs(index_0)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(index_0).call(tx_params.as_dict())

    def send_transaction(
        self, index_0: bytes, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        :param tx_params: transaction parameters

        """
        (index_0) = self.validate_and_normalize_inputs(index_0)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(index_0).transact(tx_params.as_dict())

    def estimate_gas(
        self, index_0: bytes, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (index_0) = self.validate_and_normalize_inputs(index_0)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(index_0).estimateGas(tx_params.as_dict())


class AddAuthorizedAddressMethod(ContractMethod):
    """Various interfaces to the addAuthorizedAddress method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def validate_and_normalize_inputs(self, target: str):
        """Validate the inputs to the addAuthorizedAddress method."""
        self.validator.assert_valid(
            method_name="addAuthorizedAddress",
            parameter_name="target",
            argument_value=target,
        )
        target = self.validate_and_checksum_address(target)
        return target

    def call(
        self, target: str, tx_params: Optional[TxParams] = None
    ) -> Union[None, Union[HexBytes, bytes]]:
        """Execute underlying contract method via eth_call.

        Authorizes an address.

        :param target: Address to authorize.
        :param tx_params: transaction parameters
        :returns: the return value of the underlying method.
        """
        (target) = self.validate_and_normalize_inputs(target)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(target).call(tx_params.as_dict())

    def send_transaction(
        self, target: str, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Authorizes an address.

        :param target: Address to authorize.
        :param tx_params: transaction parameters
        """
        (target) = self.validate_and_normalize_inputs(target)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(target).transact(tx_params.as_dict())

    def estimate_gas(
        self, target: str, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (target) = self.validate_and_normalize_inputs(target)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(target).estimateGas(tx_params.as_dict())


class AuthoritiesMethod(ContractMethod):
    """Various interfaces to the authorities method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def validate_and_normalize_inputs(self, index_0: int):
        """Validate the inputs to the authorities method."""
        self.validator.assert_valid(
            method_name="authorities",
            parameter_name="index_0",
            argument_value=index_0,
        )
        # safeguard against fractional inputs
        index_0 = int(index_0)
        return index_0

    def call(self, index_0: int, tx_params: Optional[TxParams] = None) -> str:
        """Execute underlying contract method via eth_call.

        :param tx_params: transaction parameters

        """
        (index_0) = self.validate_and_normalize_inputs(index_0)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(index_0).call(tx_params.as_dict())

    def send_transaction(
        self, index_0: int, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        :param tx_params: transaction parameters

        """
        (index_0) = self.validate_and_normalize_inputs(index_0)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(index_0).transact(tx_params.as_dict())

    def estimate_gas(
        self, index_0: int, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (index_0) = self.validate_and_normalize_inputs(index_0)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(index_0).estimateGas(tx_params.as_dict())


class GetAssetProxyMethod(ContractMethod):
    """Various interfaces to the getAssetProxy method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def validate_and_normalize_inputs(self, asset_proxy_id: bytes):
        """Validate the inputs to the getAssetProxy method."""
        self.validator.assert_valid(
            method_name="getAssetProxy",
            parameter_name="assetProxyId",
            argument_value=asset_proxy_id,
        )
        return asset_proxy_id

    def call(
        self, asset_proxy_id: bytes, tx_params: Optional[TxParams] = None
    ) -> str:
        """Execute underlying contract method via eth_call.

        Gets an asset proxy.

        :param assetProxyId: Id of the asset proxy.
        :param tx_params: transaction parameters
        :returns: The asset proxy registered to assetProxyId. Returns 0x0 if no
            proxy is registered.
        """
        (asset_proxy_id) = self.validate_and_normalize_inputs(asset_proxy_id)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_proxy_id).call(tx_params.as_dict())

    def send_transaction(
        self, asset_proxy_id: bytes, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Gets an asset proxy.

        :param assetProxyId: Id of the asset proxy.
        :param tx_params: transaction parameters
        :returns: The asset proxy registered to assetProxyId. Returns 0x0 if no
            proxy is registered.
        """
        (asset_proxy_id) = self.validate_and_normalize_inputs(asset_proxy_id)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_proxy_id).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self, asset_proxy_id: bytes, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (asset_proxy_id) = self.validate_and_normalize_inputs(asset_proxy_id)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_proxy_id).estimateGas(
            tx_params.as_dict()
        )


class RemoveAuthorizedAddressMethod(ContractMethod):
    """Various interfaces to the removeAuthorizedAddress method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def validate_and_normalize_inputs(self, target: str):
        """Validate the inputs to the removeAuthorizedAddress method."""
        self.validator.assert_valid(
            method_name="removeAuthorizedAddress",
            parameter_name="target",
            argument_value=target,
        )
        target = self.validate_and_checksum_address(target)
        return target

    def call(
        self, target: str, tx_params: Optional[TxParams] = None
    ) -> Union[None, Union[HexBytes, bytes]]:
        """Execute underlying contract method via eth_call.

        Removes authorizion of an address.

        :param target: Address to remove authorization from.
        :param tx_params: transaction parameters
        :returns: the return value of the underlying method.
        """
        (target) = self.validate_and_normalize_inputs(target)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(target).call(tx_params.as_dict())

    def send_transaction(
        self, target: str, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Removes authorizion of an address.

        :param target: Address to remove authorization from.
        :param tx_params: transaction parameters
        """
        (target) = self.validate_and_normalize_inputs(target)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(target).transact(tx_params.as_dict())

    def estimate_gas(
        self, target: str, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (target) = self.validate_and_normalize_inputs(target)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(target).estimateGas(tx_params.as_dict())


class OwnerMethod(ContractMethod):
    """Various interfaces to the owner method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def call(self, tx_params: Optional[TxParams] = None) -> str:
        """Execute underlying contract method via eth_call.

        :param tx_params: transaction parameters

        """
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method().call(tx_params.as_dict())

    def send_transaction(
        self, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        :param tx_params: transaction parameters

        """
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method().transact(tx_params.as_dict())

    def estimate_gas(self, tx_params: Optional[TxParams] = None) -> int:
        """Estimate gas consumption of method call."""
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method().estimateGas(tx_params.as_dict())


class RemoveAuthorizedAddressAtIndexMethod(ContractMethod):
    """Various interfaces to the removeAuthorizedAddressAtIndex method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def validate_and_normalize_inputs(self, target: str, index: int):
        """Validate the inputs to the removeAuthorizedAddressAtIndex method."""
        self.validator.assert_valid(
            method_name="removeAuthorizedAddressAtIndex",
            parameter_name="target",
            argument_value=target,
        )
        target = self.validate_and_checksum_address(target)
        self.validator.assert_valid(
            method_name="removeAuthorizedAddressAtIndex",
            parameter_name="index",
            argument_value=index,
        )
        # safeguard against fractional inputs
        index = int(index)
        return (target, index)

    def call(
        self, target: str, index: int, tx_params: Optional[TxParams] = None
    ) -> Union[None, Union[HexBytes, bytes]]:
        """Execute underlying contract method via eth_call.

        Removes authorizion of an address.

        :param index: Index of target in authorities array.
        :param target: Address to remove authorization from.
        :param tx_params: transaction parameters
        :returns: the return value of the underlying method.
        """
        (target, index) = self.validate_and_normalize_inputs(target, index)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(target, index).call(tx_params.as_dict())

    def send_transaction(
        self, target: str, index: int, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Removes authorizion of an address.

        :param index: Index of target in authorities array.
        :param target: Address to remove authorization from.
        :param tx_params: transaction parameters
        """
        (target, index) = self.validate_and_normalize_inputs(target, index)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(target, index).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self, target: str, index: int, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (target, index) = self.validate_and_normalize_inputs(target, index)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(target, index).estimateGas(
            tx_params.as_dict()
        )


class GetProxyIdMethod(ContractMethod):
    """Various interfaces to the getProxyId method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def call(self, tx_params: Optional[TxParams] = None) -> bytes:
        """Execute underlying contract method via eth_call.

        Gets the proxy id associated with the proxy address.

        :param tx_params: transaction parameters
        :returns: Proxy id.
        """
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method().call(tx_params.as_dict())

    def send_transaction(
        self, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Gets the proxy id associated with the proxy address.

        :param tx_params: transaction parameters
        :returns: Proxy id.
        """
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method().transact(tx_params.as_dict())

    def estimate_gas(self, tx_params: Optional[TxParams] = None) -> int:
        """Estimate gas consumption of method call."""
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method().estimateGas(tx_params.as_dict())


class AuthorizedMethod(ContractMethod):
    """Various interfaces to the authorized method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def validate_and_normalize_inputs(self, index_0: str):
        """Validate the inputs to the authorized method."""
        self.validator.assert_valid(
            method_name="authorized",
            parameter_name="index_0",
            argument_value=index_0,
        )
        index_0 = self.validate_and_checksum_address(index_0)
        return index_0

    def call(self, index_0: str, tx_params: Optional[TxParams] = None) -> bool:
        """Execute underlying contract method via eth_call.

        :param tx_params: transaction parameters

        """
        (index_0) = self.validate_and_normalize_inputs(index_0)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(index_0).call(tx_params.as_dict())

    def send_transaction(
        self, index_0: str, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        :param tx_params: transaction parameters

        """
        (index_0) = self.validate_and_normalize_inputs(index_0)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(index_0).transact(tx_params.as_dict())

    def estimate_gas(
        self, index_0: str, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (index_0) = self.validate_and_normalize_inputs(index_0)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(index_0).estimateGas(tx_params.as_dict())


class RegisterAssetProxyMethod(ContractMethod):
    """Various interfaces to the registerAssetProxy method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def validate_and_normalize_inputs(self, asset_proxy: str):
        """Validate the inputs to the registerAssetProxy method."""
        self.validator.assert_valid(
            method_name="registerAssetProxy",
            parameter_name="assetProxy",
            argument_value=asset_proxy,
        )
        asset_proxy = self.validate_and_checksum_address(asset_proxy)
        return asset_proxy

    def call(
        self, asset_proxy: str, tx_params: Optional[TxParams] = None
    ) -> Union[None, Union[HexBytes, bytes]]:
        """Execute underlying contract method via eth_call.

        Registers an asset proxy to its asset proxy id. Once an asset proxy is
        registered, it cannot be unregistered.

        :param assetProxy: Address of new asset proxy to register.
        :param tx_params: transaction parameters
        :returns: the return value of the underlying method.
        """
        (asset_proxy) = self.validate_and_normalize_inputs(asset_proxy)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_proxy).call(tx_params.as_dict())

    def send_transaction(
        self, asset_proxy: str, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Registers an asset proxy to its asset proxy id. Once an asset proxy is
        registered, it cannot be unregistered.

        :param assetProxy: Address of new asset proxy to register.
        :param tx_params: transaction parameters
        """
        (asset_proxy) = self.validate_and_normalize_inputs(asset_proxy)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_proxy).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self, asset_proxy: str, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (asset_proxy) = self.validate_and_normalize_inputs(asset_proxy)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_proxy).estimateGas(
            tx_params.as_dict()
        )


class GetAuthorizedAddressesMethod(ContractMethod):
    """Various interfaces to the getAuthorizedAddresses method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def call(self, tx_params: Optional[TxParams] = None) -> List[str]:
        """Execute underlying contract method via eth_call.

        Gets all authorized addresses.

        :param tx_params: transaction parameters
        :returns: Array of authorized addresses.
        """
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method().call(tx_params.as_dict())

    def send_transaction(
        self, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Gets all authorized addresses.

        :param tx_params: transaction parameters
        :returns: Array of authorized addresses.
        """
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method().transact(tx_params.as_dict())

    def estimate_gas(self, tx_params: Optional[TxParams] = None) -> int:
        """Estimate gas consumption of method call."""
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method().estimateGas(tx_params.as_dict())


class TransferOwnershipMethod(ContractMethod):
    """Various interfaces to the transferOwnership method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self.underlying_method = contract_function

    def validate_and_normalize_inputs(self, new_owner: str):
        """Validate the inputs to the transferOwnership method."""
        self.validator.assert_valid(
            method_name="transferOwnership",
            parameter_name="newOwner",
            argument_value=new_owner,
        )
        new_owner = self.validate_and_checksum_address(new_owner)
        return new_owner

    def call(
        self, new_owner: str, tx_params: Optional[TxParams] = None
    ) -> Union[None, Union[HexBytes, bytes]]:
        """Execute underlying contract method via eth_call.

        :param tx_params: transaction parameters
        :returns: the return value of the underlying method.
        """
        (new_owner) = self.validate_and_normalize_inputs(new_owner)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(new_owner).call(tx_params.as_dict())

    def send_transaction(
        self, new_owner: str, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        :param tx_params: transaction parameters
        """
        (new_owner) = self.validate_and_normalize_inputs(new_owner)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(new_owner).transact(tx_params.as_dict())

    def estimate_gas(
        self, new_owner: str, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (new_owner) = self.validate_and_normalize_inputs(new_owner)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(new_owner).estimateGas(
            tx_params.as_dict()
        )


# pylint: disable=too-many-public-methods,too-many-instance-attributes
class MultiAssetProxy:
    """Wrapper class for MultiAssetProxy Solidity contract."""

    asset_proxies: AssetProxiesMethod
    """Constructor-initialized instance of
    :class:`AssetProxiesMethod`.
    """

    add_authorized_address: AddAuthorizedAddressMethod
    """Constructor-initialized instance of
    :class:`AddAuthorizedAddressMethod`.
    """

    authorities: AuthoritiesMethod
    """Constructor-initialized instance of
    :class:`AuthoritiesMethod`.
    """

    get_asset_proxy: GetAssetProxyMethod
    """Constructor-initialized instance of
    :class:`GetAssetProxyMethod`.
    """

    remove_authorized_address: RemoveAuthorizedAddressMethod
    """Constructor-initialized instance of
    :class:`RemoveAuthorizedAddressMethod`.
    """

    owner: OwnerMethod
    """Constructor-initialized instance of
    :class:`OwnerMethod`.
    """

    remove_authorized_address_at_index: RemoveAuthorizedAddressAtIndexMethod
    """Constructor-initialized instance of
    :class:`RemoveAuthorizedAddressAtIndexMethod`.
    """

    get_proxy_id: GetProxyIdMethod
    """Constructor-initialized instance of
    :class:`GetProxyIdMethod`.
    """

    authorized: AuthorizedMethod
    """Constructor-initialized instance of
    :class:`AuthorizedMethod`.
    """

    register_asset_proxy: RegisterAssetProxyMethod
    """Constructor-initialized instance of
    :class:`RegisterAssetProxyMethod`.
    """

    get_authorized_addresses: GetAuthorizedAddressesMethod
    """Constructor-initialized instance of
    :class:`GetAuthorizedAddressesMethod`.
    """

    transfer_ownership: TransferOwnershipMethod
    """Constructor-initialized instance of
    :class:`TransferOwnershipMethod`.
    """

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        validator: MultiAssetProxyValidator = None,
    ):
        """Get an instance of wrapper for smart contract.

        :param provider: instance of :class:`web3.providers.base.BaseProvider`
        :param contract_address: where the contract has been deployed
        :param validator: for validation of method inputs.
        """
        self.contract_address = contract_address

        if not validator:
            validator = MultiAssetProxyValidator(provider, contract_address)

        self._web3_eth = Web3(  # type: ignore # pylint: disable=no-member
            provider
        ).eth

        functions = self._web3_eth.contract(
            address=to_checksum_address(contract_address),
            abi=MultiAssetProxy.abi(),
        ).functions

        self.asset_proxies = AssetProxiesMethod(
            provider, contract_address, functions.assetProxies, validator
        )

        self.add_authorized_address = AddAuthorizedAddressMethod(
            provider,
            contract_address,
            functions.addAuthorizedAddress,
            validator,
        )

        self.authorities = AuthoritiesMethod(
            provider, contract_address, functions.authorities, validator
        )

        self.get_asset_proxy = GetAssetProxyMethod(
            provider, contract_address, functions.getAssetProxy, validator
        )

        self.remove_authorized_address = RemoveAuthorizedAddressMethod(
            provider,
            contract_address,
            functions.removeAuthorizedAddress,
            validator,
        )

        self.owner = OwnerMethod(
            provider, contract_address, functions.owner, validator
        )

        self.remove_authorized_address_at_index = RemoveAuthorizedAddressAtIndexMethod(
            provider,
            contract_address,
            functions.removeAuthorizedAddressAtIndex,
            validator,
        )

        self.get_proxy_id = GetProxyIdMethod(
            provider, contract_address, functions.getProxyId, validator
        )

        self.authorized = AuthorizedMethod(
            provider, contract_address, functions.authorized, validator
        )

        self.register_asset_proxy = RegisterAssetProxyMethod(
            provider, contract_address, functions.registerAssetProxy, validator
        )

        self.get_authorized_addresses = GetAuthorizedAddressesMethod(
            provider,
            contract_address,
            functions.getAuthorizedAddresses,
            validator,
        )

        self.transfer_ownership = TransferOwnershipMethod(
            provider, contract_address, functions.transferOwnership, validator
        )

    def get_authorized_address_added_event(
        self, tx_hash: Union[HexBytes, bytes]
    ) -> Tuple[AttributeDict]:
        """Get log entry for AuthorizedAddressAdded event.

        :param tx_hash: hash of transaction emitting AuthorizedAddressAdded
            event
        """
        tx_receipt = self._web3_eth.getTransactionReceipt(tx_hash)
        return (
            self._web3_eth.contract(
                address=to_checksum_address(self.contract_address),
                abi=MultiAssetProxy.abi(),
            )
            .events.AuthorizedAddressAdded()
            .processReceipt(tx_receipt)
        )

    def get_authorized_address_removed_event(
        self, tx_hash: Union[HexBytes, bytes]
    ) -> Tuple[AttributeDict]:
        """Get log entry for AuthorizedAddressRemoved event.

        :param tx_hash: hash of transaction emitting AuthorizedAddressRemoved
            event
        """
        tx_receipt = self._web3_eth.getTransactionReceipt(tx_hash)
        return (
            self._web3_eth.contract(
                address=to_checksum_address(self.contract_address),
                abi=MultiAssetProxy.abi(),
            )
            .events.AuthorizedAddressRemoved()
            .processReceipt(tx_receipt)
        )

    def get_asset_proxy_registered_event(
        self, tx_hash: Union[HexBytes, bytes]
    ) -> Tuple[AttributeDict]:
        """Get log entry for AssetProxyRegistered event.

        :param tx_hash: hash of transaction emitting AssetProxyRegistered event
        """
        tx_receipt = self._web3_eth.getTransactionReceipt(tx_hash)
        return (
            self._web3_eth.contract(
                address=to_checksum_address(self.contract_address),
                abi=MultiAssetProxy.abi(),
            )
            .events.AssetProxyRegistered()
            .processReceipt(tx_receipt)
        )

    @staticmethod
    def abi():
        """Return the ABI to the underlying contract."""
        return json.loads(
            '[{"constant":true,"inputs":[{"name":"index_0","type":"bytes4"}],"name":"assetProxies","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"target","type":"address"}],"name":"addAuthorizedAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"index_0","type":"uint256"}],"name":"authorities","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"assetProxyId","type":"bytes4"}],"name":"getAssetProxy","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"target","type":"address"}],"name":"removeAuthorizedAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"target","type":"address"},{"name":"index","type":"uint256"}],"name":"removeAuthorizedAddressAtIndex","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getProxyId","outputs":[{"name":"","type":"bytes4"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"index_0","type":"address"}],"name":"authorized","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"assetProxy","type":"address"}],"name":"registerAssetProxy","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getAuthorizedAddresses","outputs":[{"name":"","type":"address[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"payable":false,"stateMutability":"nonpayable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"target","type":"address"},{"indexed":true,"name":"caller","type":"address"}],"name":"AuthorizedAddressAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"target","type":"address"},{"indexed":true,"name":"caller","type":"address"}],"name":"AuthorizedAddressRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"id","type":"bytes4"},{"indexed":false,"name":"assetProxy","type":"address"}],"name":"AssetProxyRegistered","type":"event"}]'  # noqa: E501 (line-too-long)
        )


# pylint: disable=too-many-lines
