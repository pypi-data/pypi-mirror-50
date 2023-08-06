"""Generated wrapper for DevUtils Solidity contract."""

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
# constructor for DevUtils below.
try:
    # both mypy and pylint complain about what we're doing here, but this
    # works just fine, so their messages have been disabled here.
    from . import (  # type: ignore # pylint: disable=import-self
        DevUtilsValidator,
    )
except ImportError:

    class DevUtilsValidator(  # type: ignore
        Validator
    ):
        """No-op input validator."""


class Tuple0x260219a2(TypedDict):
    """Python representation of a tuple or struct.

    Solidity compiler output does not include the names of structs that appear
    in method definitions.  A tuple found in an ABI may have been written in
    Solidity as a literal, anonymous tuple, or it may have been written as a
    named `struct`:code:, but there is no way to tell from the compiler
    output.  This class represents a tuple that appeared in a method
    definition.  Its name is derived from a hash of that tuple's field names,
    and every method whose ABI refers to a tuple with that same list of field
    names will have a generated wrapper method that refers to this class.

    Any members of type `bytes`:code: should be encoded as UTF-8, which can be
    accomplished via `str.encode("utf_8")`:code:
    """

    makerAddress: str

    takerAddress: str

    feeRecipientAddress: str

    senderAddress: str

    makerAssetAmount: int

    takerAssetAmount: int

    makerFee: int

    takerFee: int

    expirationTimeSeconds: int

    salt: int

    makerAssetData: bytes

    takerAssetData: bytes


class Tuple0xb1e4a1ae(TypedDict):
    """Python representation of a tuple or struct.

    Solidity compiler output does not include the names of structs that appear
    in method definitions.  A tuple found in an ABI may have been written in
    Solidity as a literal, anonymous tuple, or it may have been written as a
    named `struct`:code:, but there is no way to tell from the compiler
    output.  This class represents a tuple that appeared in a method
    definition.  Its name is derived from a hash of that tuple's field names,
    and every method whose ABI refers to a tuple with that same list of field
    names will have a generated wrapper method that refers to this class.

    Any members of type `bytes`:code: should be encoded as UTF-8, which can be
    accomplished via `str.encode("utf_8")`:code:
    """

    orderStatus: int

    orderHash: bytes

    orderTakerAssetFilledAmount: int


class DecodeErc721AssetDataMethod(ContractMethod):
    """Various interfaces to the decodeERC721AssetData method."""

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

    def validate_and_normalize_inputs(self, asset_data: bytes):
        """Validate the inputs to the decodeERC721AssetData method."""
        self.validator.assert_valid(
            method_name="decodeERC721AssetData",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = bytes.fromhex(asset_data.decode("utf-8"))
        return asset_data

    def call(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> Tuple[bytes, str, int]:
        """Execute underlying contract method via eth_call.

        Decode ERC-721 asset data from the format described in the AssetProxy
        contract specification.

        :param assetData: AssetProxy-compliant asset data describing an ERC-721
            asset.
        :param tx_params: transaction parameters
        :returns: The ERC-721 AssetProxy identifier, the address of the ERC-721
            contract hosting this asset, and the identifier of the specific
            asset to be traded.
        """
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).call(tx_params.as_dict())

    def send_transaction(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Decode ERC-721 asset data from the format described in the AssetProxy
        contract specification.

        :param assetData: AssetProxy-compliant asset data describing an ERC-721
            asset.
        :param tx_params: transaction parameters
        :returns: The ERC-721 AssetProxy identifier, the address of the ERC-721
            contract hosting this asset, and the identifier of the specific
            asset to be traded.
        """
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).transact(tx_params.as_dict())

    def estimate_gas(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).estimateGas(
            tx_params.as_dict()
        )


class GetBalanceAndAssetProxyAllowanceMethod(ContractMethod):
    """Various interfaces to the getBalanceAndAssetProxyAllowance method."""

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

    def validate_and_normalize_inputs(
        self, owner_address: str, asset_data: bytes
    ):
        """Validate the inputs to the getBalanceAndAssetProxyAllowance method."""
        self.validator.assert_valid(
            method_name="getBalanceAndAssetProxyAllowance",
            parameter_name="ownerAddress",
            argument_value=owner_address,
        )
        owner_address = self.validate_and_checksum_address(owner_address)
        self.validator.assert_valid(
            method_name="getBalanceAndAssetProxyAllowance",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = bytes.fromhex(asset_data.decode("utf-8"))
        return (owner_address, asset_data)

    def call(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> Tuple[int, int]:
        """Execute underlying contract method via eth_call.

        Calls getBalance() and getAllowance() for assetData.

        :param assetData: Details of asset, encoded per the AssetProxy contract
            specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: Number of assets (or asset baskets) held by owner, and number
            of assets (or asset baskets) that the corresponding AssetProxy is
            authorized to spend.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Calls getBalance() and getAllowance() for assetData.

        :param assetData: Details of asset, encoded per the AssetProxy contract
            specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: Number of assets (or asset baskets) held by owner, and number
            of assets (or asset baskets) that the corresponding AssetProxy is
            authorized to spend.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).estimateGas(
            tx_params.as_dict()
        )


class Erc1155ProxyIdMethod(ContractMethod):
    """Various interfaces to the ERC1155_PROXY_ID method."""

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


class GetTransferableAssetAmountMethod(ContractMethod):
    """Various interfaces to the getTransferableAssetAmount method."""

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

    def validate_and_normalize_inputs(
        self, owner_address: str, asset_data: bytes
    ):
        """Validate the inputs to the getTransferableAssetAmount method."""
        self.validator.assert_valid(
            method_name="getTransferableAssetAmount",
            parameter_name="ownerAddress",
            argument_value=owner_address,
        )
        owner_address = self.validate_and_checksum_address(owner_address)
        self.validator.assert_valid(
            method_name="getTransferableAssetAmount",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = bytes.fromhex(asset_data.decode("utf-8"))
        return (owner_address, asset_data)

    def call(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Execute underlying contract method via eth_call.

        Gets the amount of an asset transferable by the owner.

        :param assetData: Description of tokens, per the AssetProxy contract
            specification.
        :param ownerAddress: Address of the owner of the asset.
        :param tx_params: transaction parameters
        :returns: The amount of the asset tranferable by the owner. NOTE: If
            the `assetData` encodes data for multiple assets, the
            `transferableAssetAmount` will represent the amount of times the
            entire `assetData` can be transferred. To calculate the total
            individual transferable amounts, this scaled `transferableAmount`
            must be multiplied by the individual asset amounts located within
            the `assetData`.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Gets the amount of an asset transferable by the owner.

        :param assetData: Description of tokens, per the AssetProxy contract
            specification.
        :param ownerAddress: Address of the owner of the asset.
        :param tx_params: transaction parameters
        :returns: The amount of the asset tranferable by the owner. NOTE: If
            the `assetData` encodes data for multiple assets, the
            `transferableAssetAmount` will represent the amount of times the
            entire `assetData` can be transferred. To calculate the total
            individual transferable amounts, this scaled `transferableAmount`
            must be multiplied by the individual asset amounts located within
            the `assetData`.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).estimateGas(
            tx_params.as_dict()
        )


class GetBatchAssetProxyAllowancesMethod(ContractMethod):
    """Various interfaces to the getBatchAssetProxyAllowances method."""

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

    def validate_and_normalize_inputs(
        self, owner_address: str, asset_data: List[bytes]
    ):
        """Validate the inputs to the getBatchAssetProxyAllowances method."""
        self.validator.assert_valid(
            method_name="getBatchAssetProxyAllowances",
            parameter_name="ownerAddress",
            argument_value=owner_address,
        )
        owner_address = self.validate_and_checksum_address(owner_address)
        self.validator.assert_valid(
            method_name="getBatchAssetProxyAllowances",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = [
            bytes.fromhex(asset_data_element.decode("utf-8"))
            for asset_data_element in asset_data
        ]
        return (owner_address, asset_data)

    def call(
        self,
        owner_address: str,
        asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> List[int]:
        """Execute underlying contract method via eth_call.

        Calls getAssetProxyAllowance() for each element of assetData.

        :param assetData: Array of asset details, each encoded per the
            AssetProxy contract specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: An array of asset allowances from getAllowance(), with each
            element corresponding to the same-indexed element in the assetData
            input.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        owner_address: str,
        asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Calls getAssetProxyAllowance() for each element of assetData.

        :param assetData: Array of asset details, each encoded per the
            AssetProxy contract specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: An array of asset allowances from getAllowance(), with each
            element corresponding to the same-indexed element in the assetData
            input.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        owner_address: str,
        asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).estimateGas(
            tx_params.as_dict()
        )


class EncodeErc20AssetDataMethod(ContractMethod):
    """Various interfaces to the encodeERC20AssetData method."""

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

    def validate_and_normalize_inputs(self, token_address: str):
        """Validate the inputs to the encodeERC20AssetData method."""
        self.validator.assert_valid(
            method_name="encodeERC20AssetData",
            parameter_name="tokenAddress",
            argument_value=token_address,
        )
        token_address = self.validate_and_checksum_address(token_address)
        return token_address

    def call(
        self, token_address: str, tx_params: Optional[TxParams] = None
    ) -> bytes:
        """Execute underlying contract method via eth_call.

        Encode ERC-20 asset data into the format described in the AssetProxy
        contract specification.

        :param tokenAddress: The address of the ERC-20 contract hosting the
            asset to be traded.
        :param tx_params: transaction parameters
        :returns: AssetProxy-compliant data describing the asset.
        """
        (token_address) = self.validate_and_normalize_inputs(token_address)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(token_address).call(tx_params.as_dict())

    def send_transaction(
        self, token_address: str, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Encode ERC-20 asset data into the format described in the AssetProxy
        contract specification.

        :param tokenAddress: The address of the ERC-20 contract hosting the
            asset to be traded.
        :param tx_params: transaction parameters
        :returns: AssetProxy-compliant data describing the asset.
        """
        (token_address) = self.validate_and_normalize_inputs(token_address)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(token_address).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self, token_address: str, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (token_address) = self.validate_and_normalize_inputs(token_address)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(token_address).estimateGas(
            tx_params.as_dict()
        )


class DecodeZeroExTransactionDataMethod(ContractMethod):
    """Various interfaces to the decodeZeroExTransactionData method."""

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

    def validate_and_normalize_inputs(self, transaction_data: bytes):
        """Validate the inputs to the decodeZeroExTransactionData method."""
        self.validator.assert_valid(
            method_name="decodeZeroExTransactionData",
            parameter_name="transactionData",
            argument_value=transaction_data,
        )
        transaction_data = bytes.fromhex(transaction_data.decode("utf-8"))
        return transaction_data

    def call(
        self, transaction_data: bytes, tx_params: Optional[TxParams] = None
    ) -> Tuple[str, List[Tuple0x260219a2], List[int], List[bytes]]:
        """Execute underlying contract method via eth_call.

        Decodes the call data for an Exchange contract method call.

        :param transactionData: ABI-encoded calldata for an Exchange
            contract method call.
        :param tx_params: transaction parameters
        :returns: The name of the function called, and the parameters it was
            given. For single-order fills and cancels, the arrays will have
            just one element.
        """
        (transaction_data) = self.validate_and_normalize_inputs(
            transaction_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(transaction_data).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self, transaction_data: bytes, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Decodes the call data for an Exchange contract method call.

        :param transactionData: ABI-encoded calldata for an Exchange
            contract method call.
        :param tx_params: transaction parameters
        :returns: The name of the function called, and the parameters it was
            given. For single-order fills and cancels, the arrays will have
            just one element.
        """
        (transaction_data) = self.validate_and_normalize_inputs(
            transaction_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(transaction_data).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self, transaction_data: bytes, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (transaction_data) = self.validate_and_normalize_inputs(
            transaction_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(transaction_data).estimateGas(
            tx_params.as_dict()
        )


class GetBalanceMethod(ContractMethod):
    """Various interfaces to the getBalance method."""

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

    def validate_and_normalize_inputs(
        self, owner_address: str, asset_data: bytes
    ):
        """Validate the inputs to the getBalance method."""
        self.validator.assert_valid(
            method_name="getBalance",
            parameter_name="ownerAddress",
            argument_value=owner_address,
        )
        owner_address = self.validate_and_checksum_address(owner_address)
        self.validator.assert_valid(
            method_name="getBalance",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = bytes.fromhex(asset_data.decode("utf-8"))
        return (owner_address, asset_data)

    def call(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Execute underlying contract method via eth_call.

        Returns the owner's balance of the assets(s) specified in assetData.
        When the asset data contains multiple assets (eg in ERC1155 or Multi-
        Asset), the return value indicates how many complete "baskets" of those
        assets are owned by owner.

        :param assetData: Details of asset, encoded per the AssetProxy contract
            specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: Number of assets (or asset baskets) held by owner.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Returns the owner's balance of the assets(s) specified in assetData.
        When the asset data contains multiple assets (eg in ERC1155 or Multi-
        Asset), the return value indicates how many complete "baskets" of those
        assets are owned by owner.

        :param assetData: Details of asset, encoded per the AssetProxy contract
            specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: Number of assets (or asset baskets) held by owner.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).estimateGas(
            tx_params.as_dict()
        )


class GetOrderRelevantStatesMethod(ContractMethod):
    """Various interfaces to the getOrderRelevantStates method."""

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

    def validate_and_normalize_inputs(
        self, orders: List[Tuple0x260219a2], signatures: List[bytes]
    ):
        """Validate the inputs to the getOrderRelevantStates method."""
        self.validator.assert_valid(
            method_name="getOrderRelevantStates",
            parameter_name="orders",
            argument_value=orders,
        )
        self.validator.assert_valid(
            method_name="getOrderRelevantStates",
            parameter_name="signatures",
            argument_value=signatures,
        )
        signatures = [
            bytes.fromhex(signatures_element.decode("utf-8"))
            for signatures_element in signatures
        ]
        return (orders, signatures)

    def call(
        self,
        orders: List[Tuple0x260219a2],
        signatures: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> Tuple[List[Tuple0xb1e4a1ae], List[int], List[bool]]:
        """Execute underlying contract method via eth_call.

        Fetches all order-relevant information needed to validate if the
        supplied orders are fillable.

        :param orders: Array of order structures.
        :param signatures: Array of signatures provided by makers that prove
            the authenticity of the orders. `0x01` can always be provided if a
            signature does not need to be validated.
        :param tx_params: transaction parameters
        :returns: The ordersInfo (array of the hash, status, and
            `takerAssetAmount` already filled for each order),
            fillableTakerAssetAmounts (array of amounts for each order's
            `takerAssetAmount` that is fillable given all on-chain state), and
            isValidSignature (array containing the validity of each provided
            signature). NOTE: If the `takerAssetData` encodes data for multiple
            assets, each element of `fillableTakerAssetAmounts` will represent
            a "scaled" amount, meaning it must be multiplied by all the
            individual asset amounts within the `takerAssetData` to get the
            final amount of each asset that can be filled.
        """
        (orders, signatures) = self.validate_and_normalize_inputs(
            orders, signatures
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(orders, signatures).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        orders: List[Tuple0x260219a2],
        signatures: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Fetches all order-relevant information needed to validate if the
        supplied orders are fillable.

        :param orders: Array of order structures.
        :param signatures: Array of signatures provided by makers that prove
            the authenticity of the orders. `0x01` can always be provided if a
            signature does not need to be validated.
        :param tx_params: transaction parameters
        :returns: The ordersInfo (array of the hash, status, and
            `takerAssetAmount` already filled for each order),
            fillableTakerAssetAmounts (array of amounts for each order's
            `takerAssetAmount` that is fillable given all on-chain state), and
            isValidSignature (array containing the validity of each provided
            signature). NOTE: If the `takerAssetData` encodes data for multiple
            assets, each element of `fillableTakerAssetAmounts` will represent
            a "scaled" amount, meaning it must be multiplied by all the
            individual asset amounts within the `takerAssetData` to get the
            final amount of each asset that can be filled.
        """
        (orders, signatures) = self.validate_and_normalize_inputs(
            orders, signatures
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(orders, signatures).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        orders: List[Tuple0x260219a2],
        signatures: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (orders, signatures) = self.validate_and_normalize_inputs(
            orders, signatures
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(orders, signatures).estimateGas(
            tx_params.as_dict()
        )


class Erc20ProxyIdMethod(ContractMethod):
    """Various interfaces to the ERC20_PROXY_ID method."""

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


class DecodeErc20AssetDataMethod(ContractMethod):
    """Various interfaces to the decodeERC20AssetData method."""

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

    def validate_and_normalize_inputs(self, asset_data: bytes):
        """Validate the inputs to the decodeERC20AssetData method."""
        self.validator.assert_valid(
            method_name="decodeERC20AssetData",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = bytes.fromhex(asset_data.decode("utf-8"))
        return asset_data

    def call(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> Tuple[bytes, str]:
        """Execute underlying contract method via eth_call.

        Decode ERC-20 asset data from the format described in the AssetProxy
        contract specification.

        :param assetData: AssetProxy-compliant asset data describing an ERC-20
            asset.
        :param tx_params: transaction parameters
        :returns: The ERC-20 AssetProxy identifier, and the address of the ERC-
            20 contract hosting this asset.
        """
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).call(tx_params.as_dict())

    def send_transaction(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Decode ERC-20 asset data from the format described in the AssetProxy
        contract specification.

        :param assetData: AssetProxy-compliant asset data describing an ERC-20
            asset.
        :param tx_params: transaction parameters
        :returns: The ERC-20 AssetProxy identifier, and the address of the ERC-
            20 contract hosting this asset.
        """
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).transact(tx_params.as_dict())

    def estimate_gas(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).estimateGas(
            tx_params.as_dict()
        )


class GetOrderRelevantStateMethod(ContractMethod):
    """Various interfaces to the getOrderRelevantState method."""

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

    def validate_and_normalize_inputs(
        self, order: Tuple0x260219a2, signature: bytes
    ):
        """Validate the inputs to the getOrderRelevantState method."""
        self.validator.assert_valid(
            method_name="getOrderRelevantState",
            parameter_name="order",
            argument_value=order,
        )
        self.validator.assert_valid(
            method_name="getOrderRelevantState",
            parameter_name="signature",
            argument_value=signature,
        )
        signature = bytes.fromhex(signature.decode("utf-8"))
        return (order, signature)

    def call(
        self,
        order: Tuple0x260219a2,
        signature: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> Tuple[Tuple0xb1e4a1ae, int, bool]:
        """Execute underlying contract method via eth_call.

        Fetches all order-relevant information needed to validate if the
        supplied order is fillable.

        :param order: The order structure.
        :param signature: Signature provided by maker that proves the order's
            authenticity. `0x01` can always be provided if the signature does
            not need to be validated.
        :param tx_params: transaction parameters
        :returns: The orderInfo (hash, status, and `takerAssetAmount` already
            filled for the given order), fillableTakerAssetAmount (amount of
            the order's `takerAssetAmount` that is fillable given all on-chain
            state), and isValidSignature (validity of the provided signature).
            NOTE: If the `takerAssetData` encodes data for multiple assets,
            `fillableTakerAssetAmount` will represent a "scaled" amount,
            meaning it must be multiplied by all the individual asset amounts
            within the `takerAssetData` to get the final amount of each asset
            that can be filled.
        """
        (order, signature) = self.validate_and_normalize_inputs(
            order, signature
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(order, signature).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        order: Tuple0x260219a2,
        signature: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Fetches all order-relevant information needed to validate if the
        supplied order is fillable.

        :param order: The order structure.
        :param signature: Signature provided by maker that proves the order's
            authenticity. `0x01` can always be provided if the signature does
            not need to be validated.
        :param tx_params: transaction parameters
        :returns: The orderInfo (hash, status, and `takerAssetAmount` already
            filled for the given order), fillableTakerAssetAmount (amount of
            the order's `takerAssetAmount` that is fillable given all on-chain
            state), and isValidSignature (validity of the provided signature).
            NOTE: If the `takerAssetData` encodes data for multiple assets,
            `fillableTakerAssetAmount` will represent a "scaled" amount,
            meaning it must be multiplied by all the individual asset amounts
            within the `takerAssetData` to get the final amount of each asset
            that can be filled.
        """
        (order, signature) = self.validate_and_normalize_inputs(
            order, signature
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(order, signature).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        order: Tuple0x260219a2,
        signature: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (order, signature) = self.validate_and_normalize_inputs(
            order, signature
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(order, signature).estimateGas(
            tx_params.as_dict()
        )


class DecodeErc1155AssetDataMethod(ContractMethod):
    """Various interfaces to the decodeERC1155AssetData method."""

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

    def validate_and_normalize_inputs(self, asset_data: bytes):
        """Validate the inputs to the decodeERC1155AssetData method."""
        self.validator.assert_valid(
            method_name="decodeERC1155AssetData",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = bytes.fromhex(asset_data.decode("utf-8"))
        return asset_data

    def call(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> Tuple[bytes, str, List[int], List[int], bytes]:
        """Execute underlying contract method via eth_call.

        Decode ERC-1155 asset data from the format described in the AssetProxy
        contract specification.

        :param assetData: AssetProxy-compliant asset data describing an ERC-
            1155 set of assets.
        :param tx_params: transaction parameters
        :returns: The ERC-1155 AssetProxy identifier, the address of the ERC-
            1155 contract hosting the assets, an array of the identifiers of
            the assets to be traded, an array of asset amounts to be traded,
            and callback data. Each element of the arrays corresponds to the
            same-indexed element of the other array. Return values specified as
            `memory` are returned as pointers to locations within the memory of
            the input parameter `assetData`.
        """
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).call(tx_params.as_dict())

    def send_transaction(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Decode ERC-1155 asset data from the format described in the AssetProxy
        contract specification.

        :param assetData: AssetProxy-compliant asset data describing an ERC-
            1155 set of assets.
        :param tx_params: transaction parameters
        :returns: The ERC-1155 AssetProxy identifier, the address of the ERC-
            1155 contract hosting the assets, an array of the identifiers of
            the assets to be traded, an array of asset amounts to be traded,
            and callback data. Each element of the arrays corresponds to the
            same-indexed element of the other array. Return values specified as
            `memory` are returned as pointers to locations within the memory of
            the input parameter `assetData`.
        """
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).transact(tx_params.as_dict())

    def estimate_gas(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).estimateGas(
            tx_params.as_dict()
        )


class GetEthBalancesMethod(ContractMethod):
    """Various interfaces to the getEthBalances method."""

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

    def validate_and_normalize_inputs(self, addresses: List[str]):
        """Validate the inputs to the getEthBalances method."""
        self.validator.assert_valid(
            method_name="getEthBalances",
            parameter_name="addresses",
            argument_value=addresses,
        )
        return addresses

    def call(
        self, addresses: List[str], tx_params: Optional[TxParams] = None
    ) -> List[int]:
        """Execute underlying contract method via eth_call.

        Batch fetches ETH balances

        :param addresses: Array of addresses.
        :param tx_params: transaction parameters
        :returns: Array of ETH balances.
        """
        (addresses) = self.validate_and_normalize_inputs(addresses)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(addresses).call(tx_params.as_dict())

    def send_transaction(
        self, addresses: List[str], tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Batch fetches ETH balances

        :param addresses: Array of addresses.
        :param tx_params: transaction parameters
        :returns: Array of ETH balances.
        """
        (addresses) = self.validate_and_normalize_inputs(addresses)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(addresses).transact(tx_params.as_dict())

    def estimate_gas(
        self, addresses: List[str], tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (addresses) = self.validate_and_normalize_inputs(addresses)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(addresses).estimateGas(
            tx_params.as_dict()
        )


class Erc721ProxyIdMethod(ContractMethod):
    """Various interfaces to the ERC721_PROXY_ID method."""

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


class EncodeErc721AssetDataMethod(ContractMethod):
    """Various interfaces to the encodeERC721AssetData method."""

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

    def validate_and_normalize_inputs(self, token_address: str, token_id: int):
        """Validate the inputs to the encodeERC721AssetData method."""
        self.validator.assert_valid(
            method_name="encodeERC721AssetData",
            parameter_name="tokenAddress",
            argument_value=token_address,
        )
        token_address = self.validate_and_checksum_address(token_address)
        self.validator.assert_valid(
            method_name="encodeERC721AssetData",
            parameter_name="tokenId",
            argument_value=token_id,
        )
        # safeguard against fractional inputs
        token_id = int(token_id)
        return (token_address, token_id)

    def call(
        self,
        token_address: str,
        token_id: int,
        tx_params: Optional[TxParams] = None,
    ) -> bytes:
        """Execute underlying contract method via eth_call.

        Encode ERC-721 asset data into the format described in the AssetProxy
        specification.

        :param tokenAddress: The address of the ERC-721 contract hosting the
            asset to be traded.
        :param tokenId: The identifier of the specific asset to be traded.
        :param tx_params: transaction parameters
        :returns: AssetProxy-compliant asset data describing the asset.
        """
        (token_address, token_id) = self.validate_and_normalize_inputs(
            token_address, token_id
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(token_address, token_id).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        token_address: str,
        token_id: int,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Encode ERC-721 asset data into the format described in the AssetProxy
        specification.

        :param tokenAddress: The address of the ERC-721 contract hosting the
            asset to be traded.
        :param tokenId: The identifier of the specific asset to be traded.
        :param tx_params: transaction parameters
        :returns: AssetProxy-compliant asset data describing the asset.
        """
        (token_address, token_id) = self.validate_and_normalize_inputs(
            token_address, token_id
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(token_address, token_id).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        token_address: str,
        token_id: int,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (token_address, token_id) = self.validate_and_normalize_inputs(
            token_address, token_id
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(token_address, token_id).estimateGas(
            tx_params.as_dict()
        )


class MultiAssetProxyIdMethod(ContractMethod):
    """Various interfaces to the MULTI_ASSET_PROXY_ID method."""

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


class EncodeErc1155AssetDataMethod(ContractMethod):
    """Various interfaces to the encodeERC1155AssetData method."""

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

    def validate_and_normalize_inputs(
        self,
        token_address: str,
        token_ids: List[int],
        token_values: List[int],
        callback_data: bytes,
    ):
        """Validate the inputs to the encodeERC1155AssetData method."""
        self.validator.assert_valid(
            method_name="encodeERC1155AssetData",
            parameter_name="tokenAddress",
            argument_value=token_address,
        )
        token_address = self.validate_and_checksum_address(token_address)
        self.validator.assert_valid(
            method_name="encodeERC1155AssetData",
            parameter_name="tokenIds",
            argument_value=token_ids,
        )
        self.validator.assert_valid(
            method_name="encodeERC1155AssetData",
            parameter_name="tokenValues",
            argument_value=token_values,
        )
        self.validator.assert_valid(
            method_name="encodeERC1155AssetData",
            parameter_name="callbackData",
            argument_value=callback_data,
        )
        callback_data = bytes.fromhex(callback_data.decode("utf-8"))
        return (token_address, token_ids, token_values, callback_data)

    def call(
        self,
        token_address: str,
        token_ids: List[int],
        token_values: List[int],
        callback_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> bytes:
        """Execute underlying contract method via eth_call.

        Encode ERC-1155 asset data into the format described in the AssetProxy
        contract specification.

        :param callbackData: Data to be passed to receiving contracts when a
            transfer is performed.
        :param tokenAddress: The address of the ERC-1155 contract hosting the
            asset(s) to be traded.
        :param tokenIds: The identifiers of the specific assets to be traded.
        :param tokenValues: The amounts of each asset to be traded.
        :param tx_params: transaction parameters
        :returns: AssetProxy-compliant asset data describing the set of assets.
        """
        (
            token_address,
            token_ids,
            token_values,
            callback_data,
        ) = self.validate_and_normalize_inputs(
            token_address, token_ids, token_values, callback_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            token_address, token_ids, token_values, callback_data
        ).call(tx_params.as_dict())

    def send_transaction(
        self,
        token_address: str,
        token_ids: List[int],
        token_values: List[int],
        callback_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Encode ERC-1155 asset data into the format described in the AssetProxy
        contract specification.

        :param callbackData: Data to be passed to receiving contracts when a
            transfer is performed.
        :param tokenAddress: The address of the ERC-1155 contract hosting the
            asset(s) to be traded.
        :param tokenIds: The identifiers of the specific assets to be traded.
        :param tokenValues: The amounts of each asset to be traded.
        :param tx_params: transaction parameters
        :returns: AssetProxy-compliant asset data describing the set of assets.
        """
        (
            token_address,
            token_ids,
            token_values,
            callback_data,
        ) = self.validate_and_normalize_inputs(
            token_address, token_ids, token_values, callback_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            token_address, token_ids, token_values, callback_data
        ).transact(tx_params.as_dict())

    def estimate_gas(
        self,
        token_address: str,
        token_ids: List[int],
        token_values: List[int],
        callback_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (
            token_address,
            token_ids,
            token_values,
            callback_data,
        ) = self.validate_and_normalize_inputs(
            token_address, token_ids, token_values, callback_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            token_address, token_ids, token_values, callback_data
        ).estimateGas(tx_params.as_dict())


class GetErc721TokenOwnerMethod(ContractMethod):
    """Various interfaces to the getERC721TokenOwner method."""

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

    def validate_and_normalize_inputs(self, token_address: str, token_id: int):
        """Validate the inputs to the getERC721TokenOwner method."""
        self.validator.assert_valid(
            method_name="getERC721TokenOwner",
            parameter_name="tokenAddress",
            argument_value=token_address,
        )
        token_address = self.validate_and_checksum_address(token_address)
        self.validator.assert_valid(
            method_name="getERC721TokenOwner",
            parameter_name="tokenId",
            argument_value=token_id,
        )
        # safeguard against fractional inputs
        token_id = int(token_id)
        return (token_address, token_id)

    def call(
        self,
        token_address: str,
        token_id: int,
        tx_params: Optional[TxParams] = None,
    ) -> str:
        """Execute underlying contract method via eth_call.

        Calls `asset.ownerOf(tokenId)`, but returns a null owner instead of
        reverting on an unowned asset.

        :param tokenAddress: Address of ERC721 asset.
        :param tokenId: The identifier for the specific NFT.
        :param tx_params: transaction parameters
        :returns: Owner of tokenId or null address if unowned.
        """
        (token_address, token_id) = self.validate_and_normalize_inputs(
            token_address, token_id
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(token_address, token_id).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        token_address: str,
        token_id: int,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Calls `asset.ownerOf(tokenId)`, but returns a null owner instead of
        reverting on an unowned asset.

        :param tokenAddress: Address of ERC721 asset.
        :param tokenId: The identifier for the specific NFT.
        :param tx_params: transaction parameters
        :returns: Owner of tokenId or null address if unowned.
        """
        (token_address, token_id) = self.validate_and_normalize_inputs(
            token_address, token_id
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(token_address, token_id).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        token_address: str,
        token_id: int,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (token_address, token_id) = self.validate_and_normalize_inputs(
            token_address, token_id
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(token_address, token_id).estimateGas(
            tx_params.as_dict()
        )


class DecodeMultiAssetDataMethod(ContractMethod):
    """Various interfaces to the decodeMultiAssetData method."""

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

    def validate_and_normalize_inputs(self, asset_data: bytes):
        """Validate the inputs to the decodeMultiAssetData method."""
        self.validator.assert_valid(
            method_name="decodeMultiAssetData",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = bytes.fromhex(asset_data.decode("utf-8"))
        return asset_data

    def call(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> Tuple[bytes, List[int], List[bytes]]:
        """Execute underlying contract method via eth_call.

        Decode multi-asset data from the format described in the AssetProxy
        contract specification.

        :param assetData: AssetProxy-compliant data describing a multi-asset
            basket.
        :param tx_params: transaction parameters
        :returns: The Multi-Asset AssetProxy identifier, an array of the
            amounts of the assets to be traded, and an array of the AssetProxy-
            compliant data describing each asset to be traded. Each element of
            the arrays corresponds to the same-indexed element of the other
            array.
        """
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).call(tx_params.as_dict())

    def send_transaction(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Decode multi-asset data from the format described in the AssetProxy
        contract specification.

        :param assetData: AssetProxy-compliant data describing a multi-asset
            basket.
        :param tx_params: transaction parameters
        :returns: The Multi-Asset AssetProxy identifier, an array of the
            amounts of the assets to be traded, and an array of the AssetProxy-
            compliant data describing each asset to be traded. Each element of
            the arrays corresponds to the same-indexed element of the other
            array.
        """
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).transact(tx_params.as_dict())

    def estimate_gas(
        self, asset_data: bytes, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (asset_data) = self.validate_and_normalize_inputs(asset_data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data).estimateGas(
            tx_params.as_dict()
        )


class GetBatchBalancesMethod(ContractMethod):
    """Various interfaces to the getBatchBalances method."""

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

    def validate_and_normalize_inputs(
        self, owner_address: str, asset_data: List[bytes]
    ):
        """Validate the inputs to the getBatchBalances method."""
        self.validator.assert_valid(
            method_name="getBatchBalances",
            parameter_name="ownerAddress",
            argument_value=owner_address,
        )
        owner_address = self.validate_and_checksum_address(owner_address)
        self.validator.assert_valid(
            method_name="getBatchBalances",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = [
            bytes.fromhex(asset_data_element.decode("utf-8"))
            for asset_data_element in asset_data
        ]
        return (owner_address, asset_data)

    def call(
        self,
        owner_address: str,
        asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> List[int]:
        """Execute underlying contract method via eth_call.

        Calls getBalance() for each element of assetData.

        :param assetData: Array of asset details, each encoded per the
            AssetProxy contract specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: Array of asset balances from getBalance(), with each element
            corresponding to the same-indexed element in the assetData input.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        owner_address: str,
        asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Calls getBalance() for each element of assetData.

        :param assetData: Array of asset details, each encoded per the
            AssetProxy contract specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: Array of asset balances from getBalance(), with each element
            corresponding to the same-indexed element in the assetData input.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        owner_address: str,
        asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).estimateGas(
            tx_params.as_dict()
        )


class GetAssetProxyAllowanceMethod(ContractMethod):
    """Various interfaces to the getAssetProxyAllowance method."""

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

    def validate_and_normalize_inputs(
        self, owner_address: str, asset_data: bytes
    ):
        """Validate the inputs to the getAssetProxyAllowance method."""
        self.validator.assert_valid(
            method_name="getAssetProxyAllowance",
            parameter_name="ownerAddress",
            argument_value=owner_address,
        )
        owner_address = self.validate_and_checksum_address(owner_address)
        self.validator.assert_valid(
            method_name="getAssetProxyAllowance",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = bytes.fromhex(asset_data.decode("utf-8"))
        return (owner_address, asset_data)

    def call(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Execute underlying contract method via eth_call.

        Returns the number of asset(s) (described by assetData) that the
        corresponding AssetProxy contract is authorized to spend. When the
        asset data contains multiple assets (eg for Multi-Asset), the return
        value indicates how many complete "baskets" of those assets may be
        spent by all of the corresponding AssetProxy contracts.

        :param assetData: Details of asset, encoded per the AssetProxy contract
            specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: Number of assets (or asset baskets) that the corresponding
            AssetProxy is authorized to spend.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Returns the number of asset(s) (described by assetData) that the
        corresponding AssetProxy contract is authorized to spend. When the
        asset data contains multiple assets (eg for Multi-Asset), the return
        value indicates how many complete "baskets" of those assets may be
        spent by all of the corresponding AssetProxy contracts.

        :param assetData: Details of asset, encoded per the AssetProxy contract
            specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: Number of assets (or asset baskets) that the corresponding
            AssetProxy is authorized to spend.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        owner_address: str,
        asset_data: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).estimateGas(
            tx_params.as_dict()
        )


class EncodeMultiAssetDataMethod(ContractMethod):
    """Various interfaces to the encodeMultiAssetData method."""

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

    def validate_and_normalize_inputs(
        self, amounts: List[int], nested_asset_data: List[bytes]
    ):
        """Validate the inputs to the encodeMultiAssetData method."""
        self.validator.assert_valid(
            method_name="encodeMultiAssetData",
            parameter_name="amounts",
            argument_value=amounts,
        )
        self.validator.assert_valid(
            method_name="encodeMultiAssetData",
            parameter_name="nestedAssetData",
            argument_value=nested_asset_data,
        )
        nested_asset_data = [
            bytes.fromhex(nested_asset_data_element.decode("utf-8"))
            for nested_asset_data_element in nested_asset_data
        ]
        return (amounts, nested_asset_data)

    def call(
        self,
        amounts: List[int],
        nested_asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> bytes:
        """Execute underlying contract method via eth_call.

        Encode data for multiple assets, per the AssetProxy contract
        specification.

        :param amounts: The amounts of each asset to be traded.
        :param nestedAssetData: AssetProxy-compliant data describing each asset
            to be traded.
        :param tx_params: transaction parameters
        :returns: AssetProxy-compliant data describing the set of assets.
        """
        (amounts, nested_asset_data) = self.validate_and_normalize_inputs(
            amounts, nested_asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(amounts, nested_asset_data).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        amounts: List[int],
        nested_asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Encode data for multiple assets, per the AssetProxy contract
        specification.

        :param amounts: The amounts of each asset to be traded.
        :param nestedAssetData: AssetProxy-compliant data describing each asset
            to be traded.
        :param tx_params: transaction parameters
        :returns: AssetProxy-compliant data describing the set of assets.
        """
        (amounts, nested_asset_data) = self.validate_and_normalize_inputs(
            amounts, nested_asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(amounts, nested_asset_data).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        amounts: List[int],
        nested_asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (amounts, nested_asset_data) = self.validate_and_normalize_inputs(
            amounts, nested_asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(amounts, nested_asset_data).estimateGas(
            tx_params.as_dict()
        )


class StaticCallProxyIdMethod(ContractMethod):
    """Various interfaces to the STATIC_CALL_PROXY_ID method."""

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


class GetBatchBalancesAndAssetProxyAllowancesMethod(ContractMethod):
    """Various interfaces to the getBatchBalancesAndAssetProxyAllowances method."""

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

    def validate_and_normalize_inputs(
        self, owner_address: str, asset_data: List[bytes]
    ):
        """Validate the inputs to the getBatchBalancesAndAssetProxyAllowances method."""
        self.validator.assert_valid(
            method_name="getBatchBalancesAndAssetProxyAllowances",
            parameter_name="ownerAddress",
            argument_value=owner_address,
        )
        owner_address = self.validate_and_checksum_address(owner_address)
        self.validator.assert_valid(
            method_name="getBatchBalancesAndAssetProxyAllowances",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = [
            bytes.fromhex(asset_data_element.decode("utf-8"))
            for asset_data_element in asset_data
        ]
        return (owner_address, asset_data)

    def call(
        self,
        owner_address: str,
        asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> Tuple[List[int], List[int]]:
        """Execute underlying contract method via eth_call.

        Calls getBatchBalances() and getBatchAllowances() for each element of
        assetData.

        :param assetData: Array of asset details, each encoded per the
            AssetProxy contract specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: An array of asset balances from getBalance(), and an array of
            asset allowances from getAllowance(), with each element
            corresponding to the same-indexed element in the assetData input.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        owner_address: str,
        asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Calls getBatchBalances() and getBatchAllowances() for each element of
        assetData.

        :param assetData: Array of asset details, each encoded per the
            AssetProxy contract specification.
        :param ownerAddress: Owner of the assets specified by assetData.
        :param tx_params: transaction parameters
        :returns: An array of asset balances from getBalance(), and an array of
            asset allowances from getAllowance(), with each element
            corresponding to the same-indexed element in the assetData input.
        """
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        owner_address: str,
        asset_data: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (owner_address, asset_data) = self.validate_and_normalize_inputs(
            owner_address, asset_data
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(owner_address, asset_data).estimateGas(
            tx_params.as_dict()
        )


# pylint: disable=too-many-public-methods,too-many-instance-attributes
class DevUtils:
    """Wrapper class for DevUtils Solidity contract.

    All method parameters of type `bytes`:code: should be encoded as UTF-8,
    which can be accomplished via `str.encode("utf_8")`:code:.
    """

    decode_erc721_asset_data: DecodeErc721AssetDataMethod
    """Constructor-initialized instance of
    :class:`DecodeErc721AssetDataMethod`.
    """

    get_balance_and_asset_proxy_allowance: GetBalanceAndAssetProxyAllowanceMethod
    """Constructor-initialized instance of
    :class:`GetBalanceAndAssetProxyAllowanceMethod`.
    """

    erc1155_proxy_id: Erc1155ProxyIdMethod
    """Constructor-initialized instance of
    :class:`Erc1155ProxyIdMethod`.
    """

    get_transferable_asset_amount: GetTransferableAssetAmountMethod
    """Constructor-initialized instance of
    :class:`GetTransferableAssetAmountMethod`.
    """

    get_batch_asset_proxy_allowances: GetBatchAssetProxyAllowancesMethod
    """Constructor-initialized instance of
    :class:`GetBatchAssetProxyAllowancesMethod`.
    """

    encode_erc20_asset_data: EncodeErc20AssetDataMethod
    """Constructor-initialized instance of
    :class:`EncodeErc20AssetDataMethod`.
    """

    decode_zero_ex_transaction_data: DecodeZeroExTransactionDataMethod
    """Constructor-initialized instance of
    :class:`DecodeZeroExTransactionDataMethod`.
    """

    get_balance: GetBalanceMethod
    """Constructor-initialized instance of
    :class:`GetBalanceMethod`.
    """

    get_order_relevant_states: GetOrderRelevantStatesMethod
    """Constructor-initialized instance of
    :class:`GetOrderRelevantStatesMethod`.
    """

    erc20_proxy_id: Erc20ProxyIdMethod
    """Constructor-initialized instance of
    :class:`Erc20ProxyIdMethod`.
    """

    decode_erc20_asset_data: DecodeErc20AssetDataMethod
    """Constructor-initialized instance of
    :class:`DecodeErc20AssetDataMethod`.
    """

    get_order_relevant_state: GetOrderRelevantStateMethod
    """Constructor-initialized instance of
    :class:`GetOrderRelevantStateMethod`.
    """

    decode_erc1155_asset_data: DecodeErc1155AssetDataMethod
    """Constructor-initialized instance of
    :class:`DecodeErc1155AssetDataMethod`.
    """

    get_eth_balances: GetEthBalancesMethod
    """Constructor-initialized instance of
    :class:`GetEthBalancesMethod`.
    """

    erc721_proxy_id: Erc721ProxyIdMethod
    """Constructor-initialized instance of
    :class:`Erc721ProxyIdMethod`.
    """

    encode_erc721_asset_data: EncodeErc721AssetDataMethod
    """Constructor-initialized instance of
    :class:`EncodeErc721AssetDataMethod`.
    """

    multi_asset_proxy_id: MultiAssetProxyIdMethod
    """Constructor-initialized instance of
    :class:`MultiAssetProxyIdMethod`.
    """

    encode_erc1155_asset_data: EncodeErc1155AssetDataMethod
    """Constructor-initialized instance of
    :class:`EncodeErc1155AssetDataMethod`.
    """

    get_erc721_token_owner: GetErc721TokenOwnerMethod
    """Constructor-initialized instance of
    :class:`GetErc721TokenOwnerMethod`.
    """

    decode_multi_asset_data: DecodeMultiAssetDataMethod
    """Constructor-initialized instance of
    :class:`DecodeMultiAssetDataMethod`.
    """

    get_batch_balances: GetBatchBalancesMethod
    """Constructor-initialized instance of
    :class:`GetBatchBalancesMethod`.
    """

    get_asset_proxy_allowance: GetAssetProxyAllowanceMethod
    """Constructor-initialized instance of
    :class:`GetAssetProxyAllowanceMethod`.
    """

    encode_multi_asset_data: EncodeMultiAssetDataMethod
    """Constructor-initialized instance of
    :class:`EncodeMultiAssetDataMethod`.
    """

    static_call_proxy_id: StaticCallProxyIdMethod
    """Constructor-initialized instance of
    :class:`StaticCallProxyIdMethod`.
    """

    get_batch_balances_and_asset_proxy_allowances: GetBatchBalancesAndAssetProxyAllowancesMethod
    """Constructor-initialized instance of
    :class:`GetBatchBalancesAndAssetProxyAllowancesMethod`.
    """

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        validator: DevUtilsValidator = None,
    ):
        """Get an instance of wrapper for smart contract.

        :param provider: instance of :class:`web3.providers.base.BaseProvider`
        :param contract_address: where the contract has been deployed
        :param validator: for validation of method inputs.
        """
        self.contract_address = contract_address

        if not validator:
            validator = DevUtilsValidator(provider, contract_address)

        self._web3_eth = Web3(  # type: ignore # pylint: disable=no-member
            provider
        ).eth

        functions = self._web3_eth.contract(
            address=to_checksum_address(contract_address), abi=DevUtils.abi()
        ).functions

        self.decode_erc721_asset_data = DecodeErc721AssetDataMethod(
            provider,
            contract_address,
            functions.decodeERC721AssetData,
            validator,
        )

        self.get_balance_and_asset_proxy_allowance = GetBalanceAndAssetProxyAllowanceMethod(
            provider,
            contract_address,
            functions.getBalanceAndAssetProxyAllowance,
            validator,
        )

        self.erc1155_proxy_id = Erc1155ProxyIdMethod(
            provider, contract_address, functions.ERC1155_PROXY_ID, validator
        )

        self.get_transferable_asset_amount = GetTransferableAssetAmountMethod(
            provider,
            contract_address,
            functions.getTransferableAssetAmount,
            validator,
        )

        self.get_batch_asset_proxy_allowances = GetBatchAssetProxyAllowancesMethod(
            provider,
            contract_address,
            functions.getBatchAssetProxyAllowances,
            validator,
        )

        self.encode_erc20_asset_data = EncodeErc20AssetDataMethod(
            provider,
            contract_address,
            functions.encodeERC20AssetData,
            validator,
        )

        self.decode_zero_ex_transaction_data = DecodeZeroExTransactionDataMethod(
            provider,
            contract_address,
            functions.decodeZeroExTransactionData,
            validator,
        )

        self.get_balance = GetBalanceMethod(
            provider, contract_address, functions.getBalance, validator
        )

        self.get_order_relevant_states = GetOrderRelevantStatesMethod(
            provider,
            contract_address,
            functions.getOrderRelevantStates,
            validator,
        )

        self.erc20_proxy_id = Erc20ProxyIdMethod(
            provider, contract_address, functions.ERC20_PROXY_ID, validator
        )

        self.decode_erc20_asset_data = DecodeErc20AssetDataMethod(
            provider,
            contract_address,
            functions.decodeERC20AssetData,
            validator,
        )

        self.get_order_relevant_state = GetOrderRelevantStateMethod(
            provider,
            contract_address,
            functions.getOrderRelevantState,
            validator,
        )

        self.decode_erc1155_asset_data = DecodeErc1155AssetDataMethod(
            provider,
            contract_address,
            functions.decodeERC1155AssetData,
            validator,
        )

        self.get_eth_balances = GetEthBalancesMethod(
            provider, contract_address, functions.getEthBalances, validator
        )

        self.erc721_proxy_id = Erc721ProxyIdMethod(
            provider, contract_address, functions.ERC721_PROXY_ID, validator
        )

        self.encode_erc721_asset_data = EncodeErc721AssetDataMethod(
            provider,
            contract_address,
            functions.encodeERC721AssetData,
            validator,
        )

        self.multi_asset_proxy_id = MultiAssetProxyIdMethod(
            provider,
            contract_address,
            functions.MULTI_ASSET_PROXY_ID,
            validator,
        )

        self.encode_erc1155_asset_data = EncodeErc1155AssetDataMethod(
            provider,
            contract_address,
            functions.encodeERC1155AssetData,
            validator,
        )

        self.get_erc721_token_owner = GetErc721TokenOwnerMethod(
            provider,
            contract_address,
            functions.getERC721TokenOwner,
            validator,
        )

        self.decode_multi_asset_data = DecodeMultiAssetDataMethod(
            provider,
            contract_address,
            functions.decodeMultiAssetData,
            validator,
        )

        self.get_batch_balances = GetBatchBalancesMethod(
            provider, contract_address, functions.getBatchBalances, validator
        )

        self.get_asset_proxy_allowance = GetAssetProxyAllowanceMethod(
            provider,
            contract_address,
            functions.getAssetProxyAllowance,
            validator,
        )

        self.encode_multi_asset_data = EncodeMultiAssetDataMethod(
            provider,
            contract_address,
            functions.encodeMultiAssetData,
            validator,
        )

        self.static_call_proxy_id = StaticCallProxyIdMethod(
            provider,
            contract_address,
            functions.STATIC_CALL_PROXY_ID,
            validator,
        )

        self.get_batch_balances_and_asset_proxy_allowances = GetBatchBalancesAndAssetProxyAllowancesMethod(
            provider,
            contract_address,
            functions.getBatchBalancesAndAssetProxyAllowances,
            validator,
        )

    @staticmethod
    def abi():
        """Return the ABI to the underlying contract."""
        return json.loads(
            '[{"constant":true,"inputs":[{"name":"assetData","type":"bytes"}],"name":"decodeERC721AssetData","outputs":[{"name":"assetProxyId","type":"bytes4"},{"name":"tokenAddress","type":"address"},{"name":"tokenId","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"ownerAddress","type":"address"},{"name":"assetData","type":"bytes"}],"name":"getBalanceAndAssetProxyAllowance","outputs":[{"name":"balance","type":"uint256"},{"name":"allowance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"ERC1155_PROXY_ID","outputs":[{"name":"","type":"bytes4"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"ownerAddress","type":"address"},{"name":"assetData","type":"bytes"}],"name":"getTransferableAssetAmount","outputs":[{"name":"transferableAssetAmount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"ownerAddress","type":"address"},{"name":"assetData","type":"bytes[]"}],"name":"getBatchAssetProxyAllowances","outputs":[{"name":"allowances","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenAddress","type":"address"}],"name":"encodeERC20AssetData","outputs":[{"name":"assetData","type":"bytes"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"transactionData","type":"bytes"}],"name":"decodeZeroExTransactionData","outputs":[{"name":"functionName","type":"string"},{"components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"orders","type":"tuple[]"},{"name":"takerAssetFillAmounts","type":"uint256[]"},{"name":"signatures","type":"bytes[]"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"ownerAddress","type":"address"},{"name":"assetData","type":"bytes"}],"name":"getBalance","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"orders","type":"tuple[]"},{"name":"signatures","type":"bytes[]"}],"name":"getOrderRelevantStates","outputs":[{"components":[{"name":"orderStatus","type":"uint8"},{"name":"orderHash","type":"bytes32"},{"name":"orderTakerAssetFilledAmount","type":"uint256"}],"name":"ordersInfo","type":"tuple[]"},{"name":"fillableTakerAssetAmounts","type":"uint256[]"},{"name":"isValidSignature","type":"bool[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"ERC20_PROXY_ID","outputs":[{"name":"","type":"bytes4"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"assetData","type":"bytes"}],"name":"decodeERC20AssetData","outputs":[{"name":"assetProxyId","type":"bytes4"},{"name":"tokenAddress","type":"address"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"order","type":"tuple"},{"name":"signature","type":"bytes"}],"name":"getOrderRelevantState","outputs":[{"components":[{"name":"orderStatus","type":"uint8"},{"name":"orderHash","type":"bytes32"},{"name":"orderTakerAssetFilledAmount","type":"uint256"}],"name":"orderInfo","type":"tuple"},{"name":"fillableTakerAssetAmount","type":"uint256"},{"name":"isValidSignature","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"assetData","type":"bytes"}],"name":"decodeERC1155AssetData","outputs":[{"name":"assetProxyId","type":"bytes4"},{"name":"tokenAddress","type":"address"},{"name":"tokenIds","type":"uint256[]"},{"name":"tokenValues","type":"uint256[]"},{"name":"callbackData","type":"bytes"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"addresses","type":"address[]"}],"name":"getEthBalances","outputs":[{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"ERC721_PROXY_ID","outputs":[{"name":"","type":"bytes4"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenAddress","type":"address"},{"name":"tokenId","type":"uint256"}],"name":"encodeERC721AssetData","outputs":[{"name":"assetData","type":"bytes"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"MULTI_ASSET_PROXY_ID","outputs":[{"name":"","type":"bytes4"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenAddress","type":"address"},{"name":"tokenIds","type":"uint256[]"},{"name":"tokenValues","type":"uint256[]"},{"name":"callbackData","type":"bytes"}],"name":"encodeERC1155AssetData","outputs":[{"name":"assetData","type":"bytes"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"tokenAddress","type":"address"},{"name":"tokenId","type":"uint256"}],"name":"getERC721TokenOwner","outputs":[{"name":"ownerAddress","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"assetData","type":"bytes"}],"name":"decodeMultiAssetData","outputs":[{"name":"assetProxyId","type":"bytes4"},{"name":"amounts","type":"uint256[]"},{"name":"nestedAssetData","type":"bytes[]"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"ownerAddress","type":"address"},{"name":"assetData","type":"bytes[]"}],"name":"getBatchBalances","outputs":[{"name":"balances","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"ownerAddress","type":"address"},{"name":"assetData","type":"bytes"}],"name":"getAssetProxyAllowance","outputs":[{"name":"allowance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"amounts","type":"uint256[]"},{"name":"nestedAssetData","type":"bytes[]"}],"name":"encodeMultiAssetData","outputs":[{"name":"assetData","type":"bytes"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"STATIC_CALL_PROXY_ID","outputs":[{"name":"","type":"bytes4"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"ownerAddress","type":"address"},{"name":"assetData","type":"bytes[]"}],"name":"getBatchBalancesAndAssetProxyAllowances","outputs":[{"name":"balances","type":"uint256[]"},{"name":"allowances","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_exchange","type":"address"},{"name":"_zrxAssetData","type":"bytes"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]'  # noqa: E501 (line-too-long)
        )


# pylint: disable=too-many-lines
