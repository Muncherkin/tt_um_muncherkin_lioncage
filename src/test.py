import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles


segments = [ 63, 6, 91, 79, 102, 109, 125, 7, 127, 111 ]

@cocotb.test()
async def test_lioncage(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    G1 = 0b0000100
    G2 = 0b0001000

    # reset
    dut._log.info("reset")
    dut.rst_n.value = 0

    # end reset
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    assert dut.uio_oe == 0
    assert dut.uo_out == 0b0111111

    dut._log.info("One lion moving out")
    dut.uio_in.value = G1
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = G1|G2
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = G2 
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = 0

    assert dut.uo_out == 0b0000110


    dut._log.info("One lion moving in")
    dut.uio_in.value = G2
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = G1|G2
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = G1 
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = 0

    assert dut.uo_out == 0b0111111
    
    await ClockCycles(dut.clk, 10)

    dut._log.info("One lion reversing")
    dut.uio_in = G2
    await ClockCycles(dut.clk, 10)

    #Checking if it counted up as the lion poked its nose in
    assert dut.uo_out == 0b0000110
    await ClockCycles(dut.clk, 10)

    #Making sure it counted down once the lion was fully back in the cage
    dut.uio_in.value = G1|G2
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = G1 
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = 0

    assert dut.uo_out == 0b0111111

    await ClockCycles(dut.clk, 10)
    dut._log.info("One too many lions moving in causing underflow")
    dut.uio_in.value = G2
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = G1|G2
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = G1 
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = 0

    assert dut.uo_out == 0b1110001
