"""Generated wrapper for Coordinator Solidity contract."""

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
# constructor for Coordinator below.
try:
    # both mypy and pylint complain about what we're doing here, but this
    # works just fine, so their messages have been disabled here.
    from . import (  # type: ignore # pylint: disable=import-self
        CoordinatorValidator,
    )
except ImportError:

    class CoordinatorValidator(  # type: ignore
        Validator
    ):
        """No-op input validator."""


class Tuple0xa1ae4ec4(TypedDict):
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

    salt: int

    signerAddress: str

    data: bytes


class Tuple0x621bd3c4(TypedDict):
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

    txOrigin: str

    transactionHash: bytes

    transactionSignature: bytes

    approvalExpirationTimeSeconds: int


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


class GetSignerAddressMethod(ContractMethod):
    """Various interfaces to the getSignerAddress method."""

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

    def validate_and_normalize_inputs(self, _hash: bytes, signature: bytes):
        """Validate the inputs to the getSignerAddress method."""
        self.validator.assert_valid(
            method_name="getSignerAddress",
            parameter_name="hash",
            argument_value=_hash,
        )
        self.validator.assert_valid(
            method_name="getSignerAddress",
            parameter_name="signature",
            argument_value=signature,
        )
        signature = bytes.fromhex(signature.decode("utf-8"))
        return (_hash, signature)

    def call(
        self,
        _hash: bytes,
        signature: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> str:
        """Execute underlying contract method via eth_call.

        Recovers the address of a signer given a hash and signature.

        :param hash: Any 32 byte hash.
        :param signature: Proof that the hash has been signed by signer.
        :param tx_params: transaction parameters

        """
        (_hash, signature) = self.validate_and_normalize_inputs(
            _hash, signature
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(_hash, signature).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        _hash: bytes,
        signature: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Recovers the address of a signer given a hash and signature.

        :param hash: Any 32 byte hash.
        :param signature: Proof that the hash has been signed by signer.
        :param tx_params: transaction parameters

        """
        (_hash, signature) = self.validate_and_normalize_inputs(
            _hash, signature
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(_hash, signature).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        _hash: bytes,
        signature: bytes,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (_hash, signature) = self.validate_and_normalize_inputs(
            _hash, signature
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(_hash, signature).estimateGas(
            tx_params.as_dict()
        )


class GetTransactionHashMethod(ContractMethod):
    """Various interfaces to the getTransactionHash method."""

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

    def validate_and_normalize_inputs(self, transaction: Tuple0xa1ae4ec4):
        """Validate the inputs to the getTransactionHash method."""
        self.validator.assert_valid(
            method_name="getTransactionHash",
            parameter_name="transaction",
            argument_value=transaction,
        )
        return transaction

    def call(
        self,
        transaction: Tuple0xa1ae4ec4,
        tx_params: Optional[TxParams] = None,
    ) -> bytes:
        """Execute underlying contract method via eth_call.

        Calculates the EIP712 hash of a 0x transaction using the domain
        separator of the Exchange contract.

        :param transaction: 0x transaction containing salt, signerAddress, and
            data.
        :param tx_params: transaction parameters
        :returns: EIP712 hash of the transaction with the domain separator of
            this contract.
        """
        (transaction) = self.validate_and_normalize_inputs(transaction)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(transaction).call(tx_params.as_dict())

    def send_transaction(
        self,
        transaction: Tuple0xa1ae4ec4,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Calculates the EIP712 hash of a 0x transaction using the domain
        separator of the Exchange contract.

        :param transaction: 0x transaction containing salt, signerAddress, and
            data.
        :param tx_params: transaction parameters
        :returns: EIP712 hash of the transaction with the domain separator of
            this contract.
        """
        (transaction) = self.validate_and_normalize_inputs(transaction)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(transaction).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        transaction: Tuple0xa1ae4ec4,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (transaction) = self.validate_and_normalize_inputs(transaction)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(transaction).estimateGas(
            tx_params.as_dict()
        )


class GetCoordinatorApprovalHashMethod(ContractMethod):
    """Various interfaces to the getCoordinatorApprovalHash method."""

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

    def validate_and_normalize_inputs(self, approval: Tuple0x621bd3c4):
        """Validate the inputs to the getCoordinatorApprovalHash method."""
        self.validator.assert_valid(
            method_name="getCoordinatorApprovalHash",
            parameter_name="approval",
            argument_value=approval,
        )
        return approval

    def call(
        self, approval: Tuple0x621bd3c4, tx_params: Optional[TxParams] = None
    ) -> bytes:
        """Execute underlying contract method via eth_call.

        Calculated the EIP712 hash of the Coordinator approval mesasage using
        the domain separator of this contract.

        :param approval: Coordinator approval message containing the
            transaction hash, transaction signature, and expiration of the
            approval.
        :param tx_params: transaction parameters
        :returns: EIP712 hash of the Coordinator approval message with the
            domain separator of this contract.
        """
        (approval) = self.validate_and_normalize_inputs(approval)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(approval).call(tx_params.as_dict())

    def send_transaction(
        self, approval: Tuple0x621bd3c4, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Calculated the EIP712 hash of the Coordinator approval mesasage using
        the domain separator of this contract.

        :param approval: Coordinator approval message containing the
            transaction hash, transaction signature, and expiration of the
            approval.
        :param tx_params: transaction parameters
        :returns: EIP712 hash of the Coordinator approval message with the
            domain separator of this contract.
        """
        (approval) = self.validate_and_normalize_inputs(approval)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(approval).transact(tx_params.as_dict())

    def estimate_gas(
        self, approval: Tuple0x621bd3c4, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (approval) = self.validate_and_normalize_inputs(approval)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(approval).estimateGas(
            tx_params.as_dict()
        )


class ExecuteTransactionMethod(ContractMethod):
    """Various interfaces to the executeTransaction method."""

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
        transaction: Tuple0xa1ae4ec4,
        tx_origin: str,
        transaction_signature: bytes,
        approval_expiration_time_seconds: List[int],
        approval_signatures: List[bytes],
    ):
        """Validate the inputs to the executeTransaction method."""
        self.validator.assert_valid(
            method_name="executeTransaction",
            parameter_name="transaction",
            argument_value=transaction,
        )
        self.validator.assert_valid(
            method_name="executeTransaction",
            parameter_name="txOrigin",
            argument_value=tx_origin,
        )
        tx_origin = self.validate_and_checksum_address(tx_origin)
        self.validator.assert_valid(
            method_name="executeTransaction",
            parameter_name="transactionSignature",
            argument_value=transaction_signature,
        )
        transaction_signature = bytes.fromhex(
            transaction_signature.decode("utf-8")
        )
        self.validator.assert_valid(
            method_name="executeTransaction",
            parameter_name="approvalExpirationTimeSeconds",
            argument_value=approval_expiration_time_seconds,
        )
        self.validator.assert_valid(
            method_name="executeTransaction",
            parameter_name="approvalSignatures",
            argument_value=approval_signatures,
        )
        approval_signatures = [
            bytes.fromhex(approval_signatures_element.decode("utf-8"))
            for approval_signatures_element in approval_signatures
        ]
        return (
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        )

    def call(
        self,
        transaction: Tuple0xa1ae4ec4,
        tx_origin: str,
        transaction_signature: bytes,
        approval_expiration_time_seconds: List[int],
        approval_signatures: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> Union[None, Union[HexBytes, bytes]]:
        """Execute underlying contract method via eth_call.

        Executes a 0x transaction that has been signed by the feeRecipients
        that correspond to each order in the transaction's Exchange calldata.

        :param approvalExpirationTimeSeconds: Array of expiration times in
            seconds for which each corresponding approval signature expires.
        :param approvalSignatures: Array of signatures that correspond to the
            feeRecipients of each order in the transaction's Exchange calldata.
        :param transaction: 0x transaction containing salt, signerAddress, and
            data.
        :param transactionSignature: Proof that the transaction has been signed
            by the signer.
        :param txOrigin: Required signer of Ethereum transaction calling this
            function.
        :param tx_params: transaction parameters
        :returns: the return value of the underlying method.
        """
        (
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ) = self.validate_and_normalize_inputs(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ).call(tx_params.as_dict())

    def send_transaction(
        self,
        transaction: Tuple0xa1ae4ec4,
        tx_origin: str,
        transaction_signature: bytes,
        approval_expiration_time_seconds: List[int],
        approval_signatures: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Executes a 0x transaction that has been signed by the feeRecipients
        that correspond to each order in the transaction's Exchange calldata.

        :param approvalExpirationTimeSeconds: Array of expiration times in
            seconds for which each corresponding approval signature expires.
        :param approvalSignatures: Array of signatures that correspond to the
            feeRecipients of each order in the transaction's Exchange calldata.
        :param transaction: 0x transaction containing salt, signerAddress, and
            data.
        :param transactionSignature: Proof that the transaction has been signed
            by the signer.
        :param txOrigin: Required signer of Ethereum transaction calling this
            function.
        :param tx_params: transaction parameters
        """
        (
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ) = self.validate_and_normalize_inputs(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ).transact(tx_params.as_dict())

    def estimate_gas(
        self,
        transaction: Tuple0xa1ae4ec4,
        tx_origin: str,
        transaction_signature: bytes,
        approval_expiration_time_seconds: List[int],
        approval_signatures: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ) = self.validate_and_normalize_inputs(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ).estimateGas(tx_params.as_dict())


class Eip712ExchangeDomainHashMethod(ContractMethod):
    """Various interfaces to the EIP712_EXCHANGE_DOMAIN_HASH method."""

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


class AssertValidCoordinatorApprovalsMethod(ContractMethod):
    """Various interfaces to the assertValidCoordinatorApprovals method."""

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
        transaction: Tuple0xa1ae4ec4,
        tx_origin: str,
        transaction_signature: bytes,
        approval_expiration_time_seconds: List[int],
        approval_signatures: List[bytes],
    ):
        """Validate the inputs to the assertValidCoordinatorApprovals method."""
        self.validator.assert_valid(
            method_name="assertValidCoordinatorApprovals",
            parameter_name="transaction",
            argument_value=transaction,
        )
        self.validator.assert_valid(
            method_name="assertValidCoordinatorApprovals",
            parameter_name="txOrigin",
            argument_value=tx_origin,
        )
        tx_origin = self.validate_and_checksum_address(tx_origin)
        self.validator.assert_valid(
            method_name="assertValidCoordinatorApprovals",
            parameter_name="transactionSignature",
            argument_value=transaction_signature,
        )
        transaction_signature = bytes.fromhex(
            transaction_signature.decode("utf-8")
        )
        self.validator.assert_valid(
            method_name="assertValidCoordinatorApprovals",
            parameter_name="approvalExpirationTimeSeconds",
            argument_value=approval_expiration_time_seconds,
        )
        self.validator.assert_valid(
            method_name="assertValidCoordinatorApprovals",
            parameter_name="approvalSignatures",
            argument_value=approval_signatures,
        )
        approval_signatures = [
            bytes.fromhex(approval_signatures_element.decode("utf-8"))
            for approval_signatures_element in approval_signatures
        ]
        return (
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        )

    def call(
        self,
        transaction: Tuple0xa1ae4ec4,
        tx_origin: str,
        transaction_signature: bytes,
        approval_expiration_time_seconds: List[int],
        approval_signatures: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> None:
        """Execute underlying contract method via eth_call.

        Validates that the 0x transaction has been approved by all of the
        feeRecipients that correspond to each order in the transaction's
        Exchange calldata.

        :param approvalExpirationTimeSeconds: Array of expiration times in
            seconds for which each corresponding approval signature expires.
        :param approvalSignatures: Array of signatures that correspond to the
            feeRecipients of each order in the transaction's Exchange calldata.
        :param transaction: 0x transaction containing salt, signerAddress, and
            data.
        :param transactionSignature: Proof that the transaction has been signed
            by the signer.
        :param txOrigin: Required signer of Ethereum transaction calling this
            function.
        :param tx_params: transaction parameters

        """
        (
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ) = self.validate_and_normalize_inputs(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ).call(tx_params.as_dict())

    def send_transaction(
        self,
        transaction: Tuple0xa1ae4ec4,
        tx_origin: str,
        transaction_signature: bytes,
        approval_expiration_time_seconds: List[int],
        approval_signatures: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Validates that the 0x transaction has been approved by all of the
        feeRecipients that correspond to each order in the transaction's
        Exchange calldata.

        :param approvalExpirationTimeSeconds: Array of expiration times in
            seconds for which each corresponding approval signature expires.
        :param approvalSignatures: Array of signatures that correspond to the
            feeRecipients of each order in the transaction's Exchange calldata.
        :param transaction: 0x transaction containing salt, signerAddress, and
            data.
        :param transactionSignature: Proof that the transaction has been signed
            by the signer.
        :param txOrigin: Required signer of Ethereum transaction calling this
            function.
        :param tx_params: transaction parameters

        """
        (
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ) = self.validate_and_normalize_inputs(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ).transact(tx_params.as_dict())

    def estimate_gas(
        self,
        transaction: Tuple0xa1ae4ec4,
        tx_origin: str,
        transaction_signature: bytes,
        approval_expiration_time_seconds: List[int],
        approval_signatures: List[bytes],
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ) = self.validate_and_normalize_inputs(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(
            transaction,
            tx_origin,
            transaction_signature,
            approval_expiration_time_seconds,
            approval_signatures,
        ).estimateGas(tx_params.as_dict())


class DecodeOrdersFromFillDataMethod(ContractMethod):
    """Various interfaces to the decodeOrdersFromFillData method."""

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

    def validate_and_normalize_inputs(self, data: bytes):
        """Validate the inputs to the decodeOrdersFromFillData method."""
        self.validator.assert_valid(
            method_name="decodeOrdersFromFillData",
            parameter_name="data",
            argument_value=data,
        )
        data = bytes.fromhex(data.decode("utf-8"))
        return data

    def call(
        self, data: bytes, tx_params: Optional[TxParams] = None
    ) -> List[Tuple0x260219a2]:
        """Execute underlying contract method via eth_call.

        Decodes the orders from Exchange calldata representing any fill method.

        :param data: Exchange calldata representing a fill method.
        :param tx_params: transaction parameters
        :returns: The orders from the Exchange calldata.
        """
        (data) = self.validate_and_normalize_inputs(data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(data).call(tx_params.as_dict())

    def send_transaction(
        self, data: bytes, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Decodes the orders from Exchange calldata representing any fill method.

        :param data: Exchange calldata representing a fill method.
        :param tx_params: transaction parameters
        :returns: The orders from the Exchange calldata.
        """
        (data) = self.validate_and_normalize_inputs(data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(data).transact(tx_params.as_dict())

    def estimate_gas(
        self, data: bytes, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (data) = self.validate_and_normalize_inputs(data)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(data).estimateGas(tx_params.as_dict())


class Eip712CoordinatorDomainHashMethod(ContractMethod):
    """Various interfaces to the EIP712_COORDINATOR_DOMAIN_HASH method."""

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


# pylint: disable=too-many-public-methods,too-many-instance-attributes
class Coordinator:
    """Wrapper class for Coordinator Solidity contract.

    All method parameters of type `bytes`:code: should be encoded as UTF-8,
    which can be accomplished via `str.encode("utf_8")`:code:.
    """

    get_signer_address: GetSignerAddressMethod
    """Constructor-initialized instance of
    :class:`GetSignerAddressMethod`.
    """

    get_transaction_hash: GetTransactionHashMethod
    """Constructor-initialized instance of
    :class:`GetTransactionHashMethod`.
    """

    get_coordinator_approval_hash: GetCoordinatorApprovalHashMethod
    """Constructor-initialized instance of
    :class:`GetCoordinatorApprovalHashMethod`.
    """

    execute_transaction: ExecuteTransactionMethod
    """Constructor-initialized instance of
    :class:`ExecuteTransactionMethod`.
    """

    eip712_exchange_domain_hash: Eip712ExchangeDomainHashMethod
    """Constructor-initialized instance of
    :class:`Eip712ExchangeDomainHashMethod`.
    """

    assert_valid_coordinator_approvals: AssertValidCoordinatorApprovalsMethod
    """Constructor-initialized instance of
    :class:`AssertValidCoordinatorApprovalsMethod`.
    """

    decode_orders_from_fill_data: DecodeOrdersFromFillDataMethod
    """Constructor-initialized instance of
    :class:`DecodeOrdersFromFillDataMethod`.
    """

    eip712_coordinator_domain_hash: Eip712CoordinatorDomainHashMethod
    """Constructor-initialized instance of
    :class:`Eip712CoordinatorDomainHashMethod`.
    """

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        validator: CoordinatorValidator = None,
    ):
        """Get an instance of wrapper for smart contract.

        :param provider: instance of :class:`web3.providers.base.BaseProvider`
        :param contract_address: where the contract has been deployed
        :param validator: for validation of method inputs.
        """
        self.contract_address = contract_address

        if not validator:
            validator = CoordinatorValidator(provider, contract_address)

        self._web3_eth = Web3(  # type: ignore # pylint: disable=no-member
            provider
        ).eth

        functions = self._web3_eth.contract(
            address=to_checksum_address(contract_address),
            abi=Coordinator.abi(),
        ).functions

        self.get_signer_address = GetSignerAddressMethod(
            provider, contract_address, functions.getSignerAddress, validator
        )

        self.get_transaction_hash = GetTransactionHashMethod(
            provider, contract_address, functions.getTransactionHash, validator
        )

        self.get_coordinator_approval_hash = GetCoordinatorApprovalHashMethod(
            provider,
            contract_address,
            functions.getCoordinatorApprovalHash,
            validator,
        )

        self.execute_transaction = ExecuteTransactionMethod(
            provider, contract_address, functions.executeTransaction, validator
        )

        self.eip712_exchange_domain_hash = Eip712ExchangeDomainHashMethod(
            provider,
            contract_address,
            functions.EIP712_EXCHANGE_DOMAIN_HASH,
            validator,
        )

        self.assert_valid_coordinator_approvals = AssertValidCoordinatorApprovalsMethod(
            provider,
            contract_address,
            functions.assertValidCoordinatorApprovals,
            validator,
        )

        self.decode_orders_from_fill_data = DecodeOrdersFromFillDataMethod(
            provider,
            contract_address,
            functions.decodeOrdersFromFillData,
            validator,
        )

        self.eip712_coordinator_domain_hash = Eip712CoordinatorDomainHashMethod(
            provider,
            contract_address,
            functions.EIP712_COORDINATOR_DOMAIN_HASH,
            validator,
        )

    @staticmethod
    def abi():
        """Return the ABI to the underlying contract."""
        return json.loads(
            '[{"constant":true,"inputs":[{"name":"hash","type":"bytes32"},{"name":"signature","type":"bytes"}],"name":"getSignerAddress","outputs":[{"name":"signerAddress","type":"address"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"components":[{"name":"salt","type":"uint256"},{"name":"signerAddress","type":"address"},{"name":"data","type":"bytes"}],"name":"transaction","type":"tuple"}],"name":"getTransactionHash","outputs":[{"name":"transactionHash","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"components":[{"name":"txOrigin","type":"address"},{"name":"transactionHash","type":"bytes32"},{"name":"transactionSignature","type":"bytes"},{"name":"approvalExpirationTimeSeconds","type":"uint256"}],"name":"approval","type":"tuple"}],"name":"getCoordinatorApprovalHash","outputs":[{"name":"approvalHash","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"components":[{"name":"salt","type":"uint256"},{"name":"signerAddress","type":"address"},{"name":"data","type":"bytes"}],"name":"transaction","type":"tuple"},{"name":"txOrigin","type":"address"},{"name":"transactionSignature","type":"bytes"},{"name":"approvalExpirationTimeSeconds","type":"uint256[]"},{"name":"approvalSignatures","type":"bytes[]"}],"name":"executeTransaction","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"EIP712_EXCHANGE_DOMAIN_HASH","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"components":[{"name":"salt","type":"uint256"},{"name":"signerAddress","type":"address"},{"name":"data","type":"bytes"}],"name":"transaction","type":"tuple"},{"name":"txOrigin","type":"address"},{"name":"transactionSignature","type":"bytes"},{"name":"approvalExpirationTimeSeconds","type":"uint256[]"},{"name":"approvalSignatures","type":"bytes[]"}],"name":"assertValidCoordinatorApprovals","outputs":[],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"data","type":"bytes"}],"name":"decodeOrdersFromFillData","outputs":[{"components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"orders","type":"tuple[]"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"EIP712_COORDINATOR_DOMAIN_HASH","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_exchange","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]'  # noqa: E501 (line-too-long)
        )


# pylint: disable=too-many-lines
