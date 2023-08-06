"""Generated wrapper for CoordinatorRegistry Solidity contract."""

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
# constructor for CoordinatorRegistry below.
try:
    # both mypy and pylint complain about what we're doing here, but this
    # works just fine, so their messages have been disabled here.
    from . import (  # type: ignore # pylint: disable=import-self
        CoordinatorRegistryValidator,
    )
except ImportError:

    class CoordinatorRegistryValidator(  # type: ignore
        Validator
    ):
        """No-op input validator."""


class SetCoordinatorEndpointMethod(ContractMethod):
    """Various interfaces to the setCoordinatorEndpoint method."""

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

    def validate_and_normalize_inputs(self, coordinator_endpoint: str):
        """Validate the inputs to the setCoordinatorEndpoint method."""
        self.validator.assert_valid(
            method_name="setCoordinatorEndpoint",
            parameter_name="coordinatorEndpoint",
            argument_value=coordinator_endpoint,
        )
        return coordinator_endpoint

    def call(
        self, coordinator_endpoint: str, tx_params: Optional[TxParams] = None
    ) -> Union[None, Union[HexBytes, bytes]]:
        """Execute underlying contract method via eth_call.

        Called by a Coordinator operator to set the endpoint of their
        Coordinator.

        :param coordinatorEndpoint: endpoint of the Coordinator.
        :param tx_params: transaction parameters
        :returns: the return value of the underlying method.
        """
        (coordinator_endpoint) = self.validate_and_normalize_inputs(
            coordinator_endpoint
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(coordinator_endpoint).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self, coordinator_endpoint: str, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Called by a Coordinator operator to set the endpoint of their
        Coordinator.

        :param coordinatorEndpoint: endpoint of the Coordinator.
        :param tx_params: transaction parameters
        """
        (coordinator_endpoint) = self.validate_and_normalize_inputs(
            coordinator_endpoint
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(coordinator_endpoint).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self, coordinator_endpoint: str, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (coordinator_endpoint) = self.validate_and_normalize_inputs(
            coordinator_endpoint
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(coordinator_endpoint).estimateGas(
            tx_params.as_dict()
        )


class GetCoordinatorEndpointMethod(ContractMethod):
    """Various interfaces to the getCoordinatorEndpoint method."""

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

    def validate_and_normalize_inputs(self, coordinator_operator: str):
        """Validate the inputs to the getCoordinatorEndpoint method."""
        self.validator.assert_valid(
            method_name="getCoordinatorEndpoint",
            parameter_name="coordinatorOperator",
            argument_value=coordinator_operator,
        )
        coordinator_operator = self.validate_and_checksum_address(
            coordinator_operator
        )
        return coordinator_operator

    def call(
        self, coordinator_operator: str, tx_params: Optional[TxParams] = None
    ) -> str:
        """Execute underlying contract method via eth_call.

        Gets the endpoint for a Coordinator.

        :param coordinatorOperator: operator of the Coordinator endpoint.
        :param tx_params: transaction parameters

        """
        (coordinator_operator) = self.validate_and_normalize_inputs(
            coordinator_operator
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(coordinator_operator).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self, coordinator_operator: str, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Gets the endpoint for a Coordinator.

        :param coordinatorOperator: operator of the Coordinator endpoint.
        :param tx_params: transaction parameters

        """
        (coordinator_operator) = self.validate_and_normalize_inputs(
            coordinator_operator
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(coordinator_operator).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self, coordinator_operator: str, tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (coordinator_operator) = self.validate_and_normalize_inputs(
            coordinator_operator
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(coordinator_operator).estimateGas(
            tx_params.as_dict()
        )


# pylint: disable=too-many-public-methods,too-many-instance-attributes
class CoordinatorRegistry:
    """Wrapper class for CoordinatorRegistry Solidity contract."""

    set_coordinator_endpoint: SetCoordinatorEndpointMethod
    """Constructor-initialized instance of
    :class:`SetCoordinatorEndpointMethod`.
    """

    get_coordinator_endpoint: GetCoordinatorEndpointMethod
    """Constructor-initialized instance of
    :class:`GetCoordinatorEndpointMethod`.
    """

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        validator: CoordinatorRegistryValidator = None,
    ):
        """Get an instance of wrapper for smart contract.

        :param provider: instance of :class:`web3.providers.base.BaseProvider`
        :param contract_address: where the contract has been deployed
        :param validator: for validation of method inputs.
        """
        self.contract_address = contract_address

        if not validator:
            validator = CoordinatorRegistryValidator(
                provider, contract_address
            )

        self._web3_eth = Web3(  # type: ignore # pylint: disable=no-member
            provider
        ).eth

        functions = self._web3_eth.contract(
            address=to_checksum_address(contract_address),
            abi=CoordinatorRegistry.abi(),
        ).functions

        self.set_coordinator_endpoint = SetCoordinatorEndpointMethod(
            provider,
            contract_address,
            functions.setCoordinatorEndpoint,
            validator,
        )

        self.get_coordinator_endpoint = GetCoordinatorEndpointMethod(
            provider,
            contract_address,
            functions.getCoordinatorEndpoint,
            validator,
        )

    def get_coordinator_endpoint_set_event(
        self, tx_hash: Union[HexBytes, bytes]
    ) -> Tuple[AttributeDict]:
        """Get log entry for CoordinatorEndpointSet event.

        :param tx_hash: hash of transaction emitting CoordinatorEndpointSet
            event
        """
        tx_receipt = self._web3_eth.getTransactionReceipt(tx_hash)
        return (
            self._web3_eth.contract(
                address=to_checksum_address(self.contract_address),
                abi=CoordinatorRegistry.abi(),
            )
            .events.CoordinatorEndpointSet()
            .processReceipt(tx_receipt)
        )

    @staticmethod
    def abi():
        """Return the ABI to the underlying contract."""
        return json.loads(
            '[{"constant":false,"inputs":[{"name":"coordinatorEndpoint","type":"string"}],"name":"setCoordinatorEndpoint","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"coordinatorOperator","type":"address"}],"name":"getCoordinatorEndpoint","outputs":[{"name":"coordinatorEndpoint","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"coordinatorOperator","type":"address"},{"indexed":false,"name":"coordinatorEndpoint","type":"string"}],"name":"CoordinatorEndpointSet","type":"event"}]'  # noqa: E501 (line-too-long)
        )


# pylint: disable=too-many-lines
