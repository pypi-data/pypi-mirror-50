"""Generated wrapper for IWallet Solidity contract."""

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
# constructor for IWallet below.
try:
    # both mypy and pylint complain about what we're doing here, but this
    # works just fine, so their messages have been disabled here.
    from . import (  # type: ignore # pylint: disable=import-self
        IWalletValidator,
    )
except ImportError:

    class IWalletValidator(  # type: ignore
        Validator
    ):
        """No-op input validator."""


class IsValidSignatureMethod(ContractMethod):
    """Various interfaces to the isValidSignature method."""

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
        """Validate the inputs to the isValidSignature method."""
        self.validator.assert_valid(
            method_name="isValidSignature",
            parameter_name="hash",
            argument_value=_hash,
        )
        self.validator.assert_valid(
            method_name="isValidSignature",
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
    ) -> bool:
        """Execute underlying contract method via eth_call.

        Verifies that a signature is valid.

        :param hash: Message hash that is signed.
        :param signature: Proof of signing.
        :param tx_params: transaction parameters
        :returns: Validity of order signature.
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

        Verifies that a signature is valid.

        :param hash: Message hash that is signed.
        :param signature: Proof of signing.
        :param tx_params: transaction parameters
        :returns: Validity of order signature.
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


# pylint: disable=too-many-public-methods,too-many-instance-attributes
class IWallet:
    """Wrapper class for IWallet Solidity contract.

    All method parameters of type `bytes`:code: should be encoded as UTF-8,
    which can be accomplished via `str.encode("utf_8")`:code:.
    """

    is_valid_signature: IsValidSignatureMethod
    """Constructor-initialized instance of
    :class:`IsValidSignatureMethod`.
    """

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        validator: IWalletValidator = None,
    ):
        """Get an instance of wrapper for smart contract.

        :param provider: instance of :class:`web3.providers.base.BaseProvider`
        :param contract_address: where the contract has been deployed
        :param validator: for validation of method inputs.
        """
        self.contract_address = contract_address

        if not validator:
            validator = IWalletValidator(provider, contract_address)

        self._web3_eth = Web3(  # type: ignore # pylint: disable=no-member
            provider
        ).eth

        functions = self._web3_eth.contract(
            address=to_checksum_address(contract_address), abi=IWallet.abi()
        ).functions

        self.is_valid_signature = IsValidSignatureMethod(
            provider, contract_address, functions.isValidSignature, validator
        )

    @staticmethod
    def abi():
        """Return the ABI to the underlying contract."""
        return json.loads(
            '[{"constant":true,"inputs":[{"name":"hash","type":"bytes32"},{"name":"signature","type":"bytes"}],"name":"isValidSignature","outputs":[{"name":"isValid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]'  # noqa: E501 (line-too-long)
        )


# pylint: disable=too-many-lines
