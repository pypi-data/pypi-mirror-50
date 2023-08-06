"""Generated wrapper for ERC20Token Solidity contract."""

from typing import Optional, Tuple, Union

from hexbytes import HexBytes
from web3.datastructures import AttributeDict
from web3.providers.base import BaseProvider

from zero_ex.contract_artifacts import abi_by_name

from ._base_contract_wrapper import BaseContractWrapper
from .tx_params import TxParams


class ERC20Token(BaseContractWrapper):
    """Wrapper class for ERC20Token Solidity contract."""

    def __init__(
        self,
        provider: BaseProvider,
        account_address: str = None,
        private_key: str = None,
    ):
        """Get an instance of wrapper for smart contract.

        :param provider: instance of :class:`web3.providers.base.BaseProvider`
        """
        super(ERC20Token, self).__init__(
            provider=provider,
            account_address=account_address,
            private_key=private_key,
        )

    def _ERC20Token(self, token_address):
        """Get an instance of the smart contract at a specific address.

        :returns: contract object
        """
        return self._contract_instance(
            address=token_address, abi=abi_by_name("ERC20Token")
        )

    def approve(
        self,
        token_address: str,
        _spender: str,
        _value: int,
        tx_params: Optional[TxParams] = None,
        view_only: bool = False,
    ) -> Union[HexBytes, bytes]:
        """Contract method `approve`.

        :param tx_params: transaction parameters
        :param view_only: whether to use transact() or call()

        :returns: transaction hash
        """
        token_address = self._validate_and_checksum_address(token_address)
        _spender = self._validate_and_checksum_address(_spender)
        # safeguard against fractional inputs
        _value = int(_value)

        # abi_encoded_args = abi_encode('approve(address,uint256)', []);

        func = self._ERC20Token(token_address).functions.approve(
            _spender,
            _value
        )
        return self._invoke_function_call(
            func=func,
            tx_params=tx_params,
            view_only=view_only
        )

    def totalSupply(
        self,
        token_address: str,
    ) -> int:
        """Contract method `totalSupply`.

        
        """
        token_address = self._validate_and_checksum_address(token_address)

        # abi_encoded_args = abi_encode('totalSupply()', []);

        func = self._ERC20Token(token_address).functions.totalSupply(
        )
        return self._invoke_function_call(
            func=func,
            tx_params=None,
            view_only=True
        )

    def transferFrom(
        self,
        token_address: str,
        _from: str,
        _to: str,
        _value: int,
        tx_params: Optional[TxParams] = None,
        view_only: bool = False,
    ) -> Union[HexBytes, bytes]:
        """Contract method `transferFrom`.

        :param tx_params: transaction parameters
        :param view_only: whether to use transact() or call()

        :returns: transaction hash
        """
        token_address = self._validate_and_checksum_address(token_address)
        _from = self._validate_and_checksum_address(_from)
        _to = self._validate_and_checksum_address(_to)
        # safeguard against fractional inputs
        _value = int(_value)

        # abi_encoded_args = abi_encode('transferFrom(address,address,uint256)', []);

        func = self._ERC20Token(token_address).functions.transferFrom(
            _from,
            _to,
            _value
        )
        return self._invoke_function_call(
            func=func,
            tx_params=tx_params,
            view_only=view_only
        )

    def balanceOf(
        self,
        token_address: str,
        _owner: str,
    ) -> int:
        """Contract method `balanceOf`.

        
        """
        token_address = self._validate_and_checksum_address(token_address)
        _owner = self._validate_and_checksum_address(_owner)

        # abi_encoded_args = abi_encode('balanceOf(address)', []);

        func = self._ERC20Token(token_address).functions.balanceOf(
            _owner
        )
        return self._invoke_function_call(
            func=func,
            tx_params=None,
            view_only=True
        )

    def transfer(
        self,
        token_address: str,
        _to: str,
        _value: int,
        tx_params: Optional[TxParams] = None,
        view_only: bool = False,
    ) -> Union[HexBytes, bytes]:
        """Contract method `transfer`.

        :param tx_params: transaction parameters
        :param view_only: whether to use transact() or call()

        :returns: transaction hash
        """
        token_address = self._validate_and_checksum_address(token_address)
        _to = self._validate_and_checksum_address(_to)
        # safeguard against fractional inputs
        _value = int(_value)

        # abi_encoded_args = abi_encode('transfer(address,uint256)', []);

        func = self._ERC20Token(token_address).functions.transfer(
            _to,
            _value
        )
        return self._invoke_function_call(
            func=func,
            tx_params=tx_params,
            view_only=view_only
        )

    def allowance(
        self,
        token_address: str,
        _owner: str,
        _spender: str,
    ) -> int:
        """Contract method `allowance`.

        
        """
        token_address = self._validate_and_checksum_address(token_address)
        _owner = self._validate_and_checksum_address(_owner)
        _spender = self._validate_and_checksum_address(_spender)

        # abi_encoded_args = abi_encode('allowance(address,address)', []);

        func = self._ERC20Token(token_address).functions.allowance(
            _owner,
            _spender
        )
        return self._invoke_function_call(
            func=func,
            tx_params=None,
            view_only=True
        )
