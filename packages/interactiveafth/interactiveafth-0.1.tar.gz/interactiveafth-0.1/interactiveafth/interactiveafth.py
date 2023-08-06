import sys

from eth_typing import Address
from eth.vm.computation import BaseComputation
from eth.vm.message import Message
from eth.vm.state import BaseState
from eth.vm.transaction_context import BaseTransactionContext

from assembler import assemble_prog
from sexp import parse_sexp

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def execute_bytecode_on_state(state: BaseState, 
                        origin: Address,
                        gas_price: int,
                        gas: int,
                        to: Address,
                        sender: Address,
                        value: int,
                        data: bytes,
                        code: bytes,
                        code_address: Address=None,
                        predefined_vals: dict={}
                        ) -> BaseComputation:
    """
    Execute raw bytecode in the context of the current state of
    the virtual machine.
    """
    if origin is None:
        origin = sender

    # Construct a message
    message = Message(
        gas=gas,
        to=to,
        sender=sender,
        value=value,
        data=data,
        code=code,
        code_address=code_address,
    )

    # Construction a tx context
    transaction_context = state.get_transaction_context_class()(
        gas_price=gas_price,
        origin=origin,
    )
    computation_instance = state.get_computation(message, transaction_context)
    computation_instance.apply_computation = apply_patched_computation
    # Execute it in the VM
    return state.get_computation(message, transaction_context).apply_computation(
        state,
        message,
        transaction_context,
        predefined_vals
    )


def apply_patched_computation(cls,
        state: BaseState,
        message: Message,
        transaction_context: BaseTransactionContext, 
        predefined_vals: dict) -> 'BaseComputation':
    """
    Perform the computation that would be triggered by the VM message.
    """
    with cls(state, message, transaction_context) as computation:
    # Early exit on pre-compiles

        if predefined_vals:
            computation._stack = predefined_vals['stack']

        precompile = computation.precompiles.get(message.code_address, NO_RESULT)
        if precompile is not NO_RESULT:
            precompile(computation)
            return computation

        show_debug2 = computation.logger.show_debug2

        opcode_lookup = computation.opcodes
        for opcode in computation.code:
            # print("OPCODE: ", opcode)
            try:
                opcode_fn = opcode_lookup[opcode]
            except KeyError:
                opcode_fn = InvalidOpcode(opcode)

            if show_debug2:
                computation.logger.debug2(
                    "OPCODE: 0x%x (%s) | pc: %s",
                    opcode,
                    opcode_fn.mnemonic,
                    max(0, computation.code.pc - 1),
                )

            try:
                opcode_fn(computation=computation)
            except Halt:
                break
        return computation


def start_afth_session(state: BaseState, 
                    origin: Address,
                    gas_price: int,
                    gas: int,
                    to: Address,
                    sender: Address,
                    value: int):
    
    stack = None
    counter = 0

    while (1):
        counter += 1
        print("--------------------------------------------")
        print('\n{}[{}]{} ActorForth: '.format(bcolors.OKGREEN, counter, bcolors.ENDC))
        buffer = ''
        while True:
            try:
                line = input()
                if not line: break
                buffer += "\n"+line
            except (EOFError, KeyboardInterrupt) as e:
                sys.exit("\nSession is over")
        bytecode = assemble_prog(parse_sexp((buffer)))
        # computation = run_bytecode(bytes(bytecode), {"stack": stack} if stack else {})


        computation = execute_bytecode_on_state(
            state=state,
            origin=origin,
            gas=gas,
            gas_price=gas_price,
            to=to,
            value=value,
            data=b"",
            code=bytes(bytecode),
            sender=sender,
            predefined_vals={"stack": stack} if stack else {}
        )
        stack = computation._stack

        # print("\n"+bcolors.HEADER+"Computation object: "+ bcolors.ENDC, computation)
        # print(bcolors.HEADER+"VM state: "+ bcolors.ENDC, vm.state)

        print("\n{}Stack: {}{}{}".format(
            bcolors.HEADER,
            bcolors.OKGREEN, 
            list(map(lambda x: int.from_bytes(x[1], byteorder="big") if type(x[1]) == bytes else x[1], computation._stack.values,)), 
            bcolors.ENDC
        ))