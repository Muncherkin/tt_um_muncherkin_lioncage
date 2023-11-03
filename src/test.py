import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

@cocotb.test()
async def test_lioncage(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # reset
    dut._log.info("reset")
    dut.rst_n.value = 0
    dut.ui_in.value = 0

    # end reset
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    assert int(dut.segments.value) == 0b0111111

    await ClockCycles(dut.clk, 10)
    dut._log.info("One lion moving out")
    dut.ui_in.value = 0b0000100
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0b0000100|0b0001000
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0b0001000 
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 10)

    assert int(dut.segments.value) == 0b0000110

    await ClockCycles(dut.clk, 10)
    dut._log.info("One lion moving in")
    dut.ui_in.value = 0b0001000
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0b0000100|0b0001000
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0b0000100 
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 10)

    assert int(dut.segments.value) == 0b0111111
    
    await ClockCycles(dut.clk, 10)

    dut._log.info("One lion reversing")
    dut.ui_in.value = 0b0000100
    await ClockCycles(dut.clk, 10)

    #Checking if it counted up as the lion poked its nose in
    assert int(dut.segments.value) == 0b0000110
    await ClockCycles(dut.clk, 10)

    #Making sure it counted down once the lion was fully back in the cage
    dut.ui_in.value = 0b0000100|0b0001000
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0b0000100 
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 10)

    assert int(dut.segments.value) == 0b0111111

    await ClockCycles(dut.clk, 10)
    dut._log.info("One too many lions moving in causing underflow")
    dut.ui_in.value = 0b0001000
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0b0000100|0b0001000
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0b0000100 
    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 10)

    assert int(dut.segments.value) == 0b1110001
