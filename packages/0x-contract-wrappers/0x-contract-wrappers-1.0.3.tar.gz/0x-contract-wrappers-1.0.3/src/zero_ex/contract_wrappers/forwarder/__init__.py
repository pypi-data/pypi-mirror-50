"""Generated wrapper for Forwarder Solidity contract."""

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
# constructor for Forwarder below.
try:
    # both mypy and pylint complain about what we're doing here, but this
    # works just fine, so their messages have been disabled here.
    from . import (  # type: ignore # pylint: disable=import-self
        ForwarderValidator,
    )
except ImportError:

    class ForwarderValidator(  # type: ignore
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


class Tuple0xbb41e5b3(TypedDict):
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

    makerAssetFilledAmount: int

    takerAssetFilledAmount: int

    makerFeePaid: int

    takerFeePaid: int


class MarketBuyOrdersWithEthMethod(ContractMethod):
    """Various interfaces to the marketBuyOrdersWithEth method."""

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
        orders: List[Tuple0x260219a2],
        maker_asset_fill_amount: int,
        signatures: List[bytes],
        fee_orders: List[Tuple0x260219a2],
        fee_signatures: List[bytes],
        fee_percentage: int,
        fee_recipient: str,
    ):
        """Validate the inputs to the marketBuyOrdersWithEth method."""
        self.validator.assert_valid(
            method_name="marketBuyOrdersWithEth",
            parameter_name="orders",
            argument_value=orders,
        )
        self.validator.assert_valid(
            method_name="marketBuyOrdersWithEth",
            parameter_name="makerAssetFillAmount",
            argument_value=maker_asset_fill_amount,
        )
        # safeguard against fractional inputs
        maker_asset_fill_amount = int(maker_asset_fill_amount)
        self.validator.assert_valid(
            method_name="marketBuyOrdersWithEth",
            parameter_name="signatures",
            argument_value=signatures,
        )
        signatures = [
            bytes.fromhex(signatures_element.decode("utf-8"))
            for signatures_element in signatures
        ]
        self.validator.assert_valid(
            method_name="marketBuyOrdersWithEth",
            parameter_name="feeOrders",
            argument_value=fee_orders,
        )
        self.validator.assert_valid(
            method_name="marketBuyOrdersWithEth",
            parameter_name="feeSignatures",
            argument_value=fee_signatures,
        )
        fee_signatures = [
            bytes.fromhex(fee_signatures_element.decode("utf-8"))
            for fee_signatures_element in fee_signatures
        ]
        self.validator.assert_valid(
            method_name="marketBuyOrdersWithEth",
            parameter_name="feePercentage",
            argument_value=fee_percentage,
        )
        # safeguard against fractional inputs
        fee_percentage = int(fee_percentage)
        self.validator.assert_valid(
            method_name="marketBuyOrdersWithEth",
            parameter_name="feeRecipient",
            argument_value=fee_recipient,
        )
        fee_recipient = self.validate_and_checksum_address(fee_recipient)
        return (
            orders,
            maker_asset_fill_amount,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        )

    def call(
        self,
        orders: List[Tuple0x260219a2],
        maker_asset_fill_amount: int,
        signatures: List[bytes],
        fee_orders: List[Tuple0x260219a2],
        fee_signatures: List[bytes],
        fee_percentage: int,
        fee_recipient: str,
        tx_params: Optional[TxParams] = None,
    ) -> Union[
        Tuple[Tuple0xbb41e5b3, Tuple0xbb41e5b3], Union[HexBytes, bytes]
    ]:
        """Execute underlying contract method via eth_call.

        Attempt to purchase makerAssetFillAmount of makerAsset by selling ETH
        provided with transaction. Any ZRX required to pay fees for primary
        orders will automatically be purchased by this contract. Any ETH not
        spent will be refunded to sender.

        :param feeOrders: Array of order specifications containing ZRX as
            makerAsset and WETH as takerAsset. Used to purchase ZRX for primary
            order fees.
        :param feePercentage: Percentage of WETH sold that will payed as fee to
            forwarding contract feeRecipient.
        :param feeRecipient: Address that will receive ETH when orders are
            filled.
        :param feeSignatures: Proofs that feeOrders have been created by
            makers.
        :param makerAssetFillAmount: Desired amount of makerAsset to purchase.
        :param orders: Array of order specifications used containing desired
            makerAsset and WETH as takerAsset.
        :param signatures: Proofs that orders have been created by makers.
        :param tx_params: transaction parameters
        :returns: the return value of the underlying method.
        """
        (
            orders,
            maker_asset_fill_amount,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ) = self.validate_and_normalize_inputs(
            orders,
            maker_asset_fill_amount,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            orders,
            maker_asset_fill_amount,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ).call(tx_params.as_dict())

    def send_transaction(
        self,
        orders: List[Tuple0x260219a2],
        maker_asset_fill_amount: int,
        signatures: List[bytes],
        fee_orders: List[Tuple0x260219a2],
        fee_signatures: List[bytes],
        fee_percentage: int,
        fee_recipient: str,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Attempt to purchase makerAssetFillAmount of makerAsset by selling ETH
        provided with transaction. Any ZRX required to pay fees for primary
        orders will automatically be purchased by this contract. Any ETH not
        spent will be refunded to sender.

        :param feeOrders: Array of order specifications containing ZRX as
            makerAsset and WETH as takerAsset. Used to purchase ZRX for primary
            order fees.
        :param feePercentage: Percentage of WETH sold that will payed as fee to
            forwarding contract feeRecipient.
        :param feeRecipient: Address that will receive ETH when orders are
            filled.
        :param feeSignatures: Proofs that feeOrders have been created by
            makers.
        :param makerAssetFillAmount: Desired amount of makerAsset to purchase.
        :param orders: Array of order specifications used containing desired
            makerAsset and WETH as takerAsset.
        :param signatures: Proofs that orders have been created by makers.
        :param tx_params: transaction parameters
        """
        (
            orders,
            maker_asset_fill_amount,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ) = self.validate_and_normalize_inputs(
            orders,
            maker_asset_fill_amount,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            orders,
            maker_asset_fill_amount,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ).transact(tx_params.as_dict())

    def estimate_gas(
        self,
        orders: List[Tuple0x260219a2],
        maker_asset_fill_amount: int,
        signatures: List[bytes],
        fee_orders: List[Tuple0x260219a2],
        fee_signatures: List[bytes],
        fee_percentage: int,
        fee_recipient: str,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (
            orders,
            maker_asset_fill_amount,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ) = self.validate_and_normalize_inputs(
            orders,
            maker_asset_fill_amount,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            orders,
            maker_asset_fill_amount,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ).estimateGas(tx_params.as_dict())


class WithdrawAssetMethod(ContractMethod):
    """Various interfaces to the withdrawAsset method."""

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

    def validate_and_normalize_inputs(self, asset_data: bytes, amount: int):
        """Validate the inputs to the withdrawAsset method."""
        self.validator.assert_valid(
            method_name="withdrawAsset",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = bytes.fromhex(asset_data.decode("utf-8"))
        self.validator.assert_valid(
            method_name="withdrawAsset",
            parameter_name="amount",
            argument_value=amount,
        )
        # safeguard against fractional inputs
        amount = int(amount)
        return (asset_data, amount)

    def call(
        self,
        asset_data: bytes,
        amount: int,
        tx_params: Optional[TxParams] = None,
    ) -> Union[None, Union[HexBytes, bytes]]:
        """Execute underlying contract method via eth_call.

        Withdraws assets from this contract. The contract requires a ZRX
        balance in order to function optimally, and this function allows the
        ZRX to be withdrawn by owner. It may also be used to withdraw assets
        that were accidentally sent to this contract.

        :param amount: Amount of ERC20 token to withdraw.
        :param assetData: Byte array encoded for the respective asset proxy.
        :param tx_params: transaction parameters
        :returns: the return value of the underlying method.
        """
        (asset_data, amount) = self.validate_and_normalize_inputs(
            asset_data, amount
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data, amount).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        asset_data: bytes,
        amount: int,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Withdraws assets from this contract. The contract requires a ZRX
        balance in order to function optimally, and this function allows the
        ZRX to be withdrawn by owner. It may also be used to withdraw assets
        that were accidentally sent to this contract.

        :param amount: Amount of ERC20 token to withdraw.
        :param assetData: Byte array encoded for the respective asset proxy.
        :param tx_params: transaction parameters
        """
        (asset_data, amount) = self.validate_and_normalize_inputs(
            asset_data, amount
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data, amount).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        asset_data: bytes,
        amount: int,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (asset_data, amount) = self.validate_and_normalize_inputs(
            asset_data, amount
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(asset_data, amount).estimateGas(
            tx_params.as_dict()
        )


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


class MarketSellOrdersWithEthMethod(ContractMethod):
    """Various interfaces to the marketSellOrdersWithEth method."""

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
        orders: List[Tuple0x260219a2],
        signatures: List[bytes],
        fee_orders: List[Tuple0x260219a2],
        fee_signatures: List[bytes],
        fee_percentage: int,
        fee_recipient: str,
    ):
        """Validate the inputs to the marketSellOrdersWithEth method."""
        self.validator.assert_valid(
            method_name="marketSellOrdersWithEth",
            parameter_name="orders",
            argument_value=orders,
        )
        self.validator.assert_valid(
            method_name="marketSellOrdersWithEth",
            parameter_name="signatures",
            argument_value=signatures,
        )
        signatures = [
            bytes.fromhex(signatures_element.decode("utf-8"))
            for signatures_element in signatures
        ]
        self.validator.assert_valid(
            method_name="marketSellOrdersWithEth",
            parameter_name="feeOrders",
            argument_value=fee_orders,
        )
        self.validator.assert_valid(
            method_name="marketSellOrdersWithEth",
            parameter_name="feeSignatures",
            argument_value=fee_signatures,
        )
        fee_signatures = [
            bytes.fromhex(fee_signatures_element.decode("utf-8"))
            for fee_signatures_element in fee_signatures
        ]
        self.validator.assert_valid(
            method_name="marketSellOrdersWithEth",
            parameter_name="feePercentage",
            argument_value=fee_percentage,
        )
        # safeguard against fractional inputs
        fee_percentage = int(fee_percentage)
        self.validator.assert_valid(
            method_name="marketSellOrdersWithEth",
            parameter_name="feeRecipient",
            argument_value=fee_recipient,
        )
        fee_recipient = self.validate_and_checksum_address(fee_recipient)
        return (
            orders,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        )

    def call(
        self,
        orders: List[Tuple0x260219a2],
        signatures: List[bytes],
        fee_orders: List[Tuple0x260219a2],
        fee_signatures: List[bytes],
        fee_percentage: int,
        fee_recipient: str,
        tx_params: Optional[TxParams] = None,
    ) -> Union[
        Tuple[Tuple0xbb41e5b3, Tuple0xbb41e5b3], Union[HexBytes, bytes]
    ]:
        """Execute underlying contract method via eth_call.

        Purchases as much of orders' makerAssets as possible by selling up to
        95% of transaction's ETH value. Any ZRX required to pay fees for
        primary orders will automatically be purchased by this contract. 5% of
        ETH value is reserved for paying fees to order feeRecipients (in ZRX)
        and forwarding contract feeRecipient (in ETH). Any ETH not spent will
        be refunded to sender.

        :param feeOrders: Array of order specifications containing ZRX as
            makerAsset and WETH as takerAsset. Used to purchase ZRX for primary
            order fees.
        :param feePercentage: Percentage of WETH sold that will payed as fee to
            forwarding contract feeRecipient.
        :param feeRecipient: Address that will receive ETH when orders are
            filled.
        :param feeSignatures: Proofs that feeOrders have been created by
            makers.
        :param orders: Array of order specifications used containing desired
            makerAsset and WETH as takerAsset.
        :param signatures: Proofs that orders have been created by makers.
        :param tx_params: transaction parameters
        :returns: the return value of the underlying method.
        """
        (
            orders,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ) = self.validate_and_normalize_inputs(
            orders,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            orders,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ).call(tx_params.as_dict())

    def send_transaction(
        self,
        orders: List[Tuple0x260219a2],
        signatures: List[bytes],
        fee_orders: List[Tuple0x260219a2],
        fee_signatures: List[bytes],
        fee_percentage: int,
        fee_recipient: str,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Purchases as much of orders' makerAssets as possible by selling up to
        95% of transaction's ETH value. Any ZRX required to pay fees for
        primary orders will automatically be purchased by this contract. 5% of
        ETH value is reserved for paying fees to order feeRecipients (in ZRX)
        and forwarding contract feeRecipient (in ETH). Any ETH not spent will
        be refunded to sender.

        :param feeOrders: Array of order specifications containing ZRX as
            makerAsset and WETH as takerAsset. Used to purchase ZRX for primary
            order fees.
        :param feePercentage: Percentage of WETH sold that will payed as fee to
            forwarding contract feeRecipient.
        :param feeRecipient: Address that will receive ETH when orders are
            filled.
        :param feeSignatures: Proofs that feeOrders have been created by
            makers.
        :param orders: Array of order specifications used containing desired
            makerAsset and WETH as takerAsset.
        :param signatures: Proofs that orders have been created by makers.
        :param tx_params: transaction parameters
        """
        (
            orders,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ) = self.validate_and_normalize_inputs(
            orders,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            orders,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ).transact(tx_params.as_dict())

    def estimate_gas(
        self,
        orders: List[Tuple0x260219a2],
        signatures: List[bytes],
        fee_orders: List[Tuple0x260219a2],
        fee_signatures: List[bytes],
        fee_percentage: int,
        fee_recipient: str,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (
            orders,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ) = self.validate_and_normalize_inputs(
            orders,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            orders,
            signatures,
            fee_orders,
            fee_signatures,
            fee_percentage,
            fee_recipient,
        ).estimateGas(tx_params.as_dict())


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
class Forwarder:
    """Wrapper class for Forwarder Solidity contract.

    All method parameters of type `bytes`:code: should be encoded as UTF-8,
    which can be accomplished via `str.encode("utf_8")`:code:.
    """

    market_buy_orders_with_eth: MarketBuyOrdersWithEthMethod
    """Constructor-initialized instance of
    :class:`MarketBuyOrdersWithEthMethod`.
    """

    withdraw_asset: WithdrawAssetMethod
    """Constructor-initialized instance of
    :class:`WithdrawAssetMethod`.
    """

    owner: OwnerMethod
    """Constructor-initialized instance of
    :class:`OwnerMethod`.
    """

    market_sell_orders_with_eth: MarketSellOrdersWithEthMethod
    """Constructor-initialized instance of
    :class:`MarketSellOrdersWithEthMethod`.
    """

    transfer_ownership: TransferOwnershipMethod
    """Constructor-initialized instance of
    :class:`TransferOwnershipMethod`.
    """

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        validator: ForwarderValidator = None,
    ):
        """Get an instance of wrapper for smart contract.

        :param provider: instance of :class:`web3.providers.base.BaseProvider`
        :param contract_address: where the contract has been deployed
        :param validator: for validation of method inputs.
        """
        self.contract_address = contract_address

        if not validator:
            validator = ForwarderValidator(provider, contract_address)

        self._web3_eth = Web3(  # type: ignore # pylint: disable=no-member
            provider
        ).eth

        functions = self._web3_eth.contract(
            address=to_checksum_address(contract_address), abi=Forwarder.abi()
        ).functions

        self.market_buy_orders_with_eth = MarketBuyOrdersWithEthMethod(
            provider,
            contract_address,
            functions.marketBuyOrdersWithEth,
            validator,
        )

        self.withdraw_asset = WithdrawAssetMethod(
            provider, contract_address, functions.withdrawAsset, validator
        )

        self.owner = OwnerMethod(
            provider, contract_address, functions.owner, validator
        )

        self.market_sell_orders_with_eth = MarketSellOrdersWithEthMethod(
            provider,
            contract_address,
            functions.marketSellOrdersWithEth,
            validator,
        )

        self.transfer_ownership = TransferOwnershipMethod(
            provider, contract_address, functions.transferOwnership, validator
        )

    @staticmethod
    def abi():
        """Return the ABI to the underlying contract."""
        return json.loads(
            '[{"constant":false,"inputs":[{"components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"orders","type":"tuple[]"},{"name":"makerAssetFillAmount","type":"uint256"},{"name":"signatures","type":"bytes[]"},{"components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"feeOrders","type":"tuple[]"},{"name":"feeSignatures","type":"bytes[]"},{"name":"feePercentage","type":"uint256"},{"name":"feeRecipient","type":"address"}],"name":"marketBuyOrdersWithEth","outputs":[{"components":[{"name":"makerAssetFilledAmount","type":"uint256"},{"name":"takerAssetFilledAmount","type":"uint256"},{"name":"makerFeePaid","type":"uint256"},{"name":"takerFeePaid","type":"uint256"}],"name":"orderFillResults","type":"tuple"},{"components":[{"name":"makerAssetFilledAmount","type":"uint256"},{"name":"takerAssetFilledAmount","type":"uint256"},{"name":"makerFeePaid","type":"uint256"},{"name":"takerFeePaid","type":"uint256"}],"name":"feeOrderFillResults","type":"tuple"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"assetData","type":"bytes"},{"name":"amount","type":"uint256"}],"name":"withdrawAsset","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"orders","type":"tuple[]"},{"name":"signatures","type":"bytes[]"},{"components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"feeOrders","type":"tuple[]"},{"name":"feeSignatures","type":"bytes[]"},{"name":"feePercentage","type":"uint256"},{"name":"feeRecipient","type":"address"}],"name":"marketSellOrdersWithEth","outputs":[{"components":[{"name":"makerAssetFilledAmount","type":"uint256"},{"name":"takerAssetFilledAmount","type":"uint256"},{"name":"makerFeePaid","type":"uint256"},{"name":"takerFeePaid","type":"uint256"}],"name":"orderFillResults","type":"tuple"},{"components":[{"name":"makerAssetFilledAmount","type":"uint256"},{"name":"takerAssetFilledAmount","type":"uint256"},{"name":"makerFeePaid","type":"uint256"},{"name":"takerFeePaid","type":"uint256"}],"name":"feeOrderFillResults","type":"tuple"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_exchange","type":"address"},{"name":"_zrxAssetData","type":"bytes"},{"name":"_wethAssetData","type":"bytes"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]'  # noqa: E501 (line-too-long)
        )


# pylint: disable=too-many-lines
