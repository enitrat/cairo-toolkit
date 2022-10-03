%lang starknet

from test.main import MyStruct
from test.types import ImportedStruct

@contract_interface
namespace IMain {
    func struct_in_arg(amount: felt, _struct: MyStruct, array_len: felt, array: felt*) {
    }

    func struct_ptr_in_return() -> (
        res_len: felt, res: felt*, arr_len: felt, arr: ImportedStruct*
    ) {
    }
}
