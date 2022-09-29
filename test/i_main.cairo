%lang starknet

from test.main import MyStruct

@contract_interface
namespace IMain {
    func increase_balance(amount: felt, test_len: felt, test: MyStruct*) {
    }

    func get_balance() -> (res: felt) {
    }
}
