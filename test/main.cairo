%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

from test.types import ImportedStruct

struct MyStruct {
    index: felt,
}

@storage_var
func storage_skipped() -> (res: felt) {
}

@external
func struct_in_arg{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    amount: felt, _struct: MyStruct, array_len: felt, array: felt*
) {
    return ();
}

@view
func struct_ptr_in_return{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (
    res_len: felt, res: felt*, arr_len: felt, arr: ImportedStruct*
) {
    return (1, new (1), 1, new ImportedStruct(0));
}

@constructor
func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() {
    return ();
}
