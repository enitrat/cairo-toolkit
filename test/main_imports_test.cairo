%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.registers import get_fp_and_pc
from starkware.cairo.common.cairo_builtins import BitwiseBuiltin
from starkware.cairo.common.math import assert_nn_le, unsigned_div_rem
from starkware.cairo.common.math_cmp import is_le
from starkware.cairo.common.memcpy import memcpy
from starkware.cairo.common.memset import memset
from starkware.cairo.common.pow import pow

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
