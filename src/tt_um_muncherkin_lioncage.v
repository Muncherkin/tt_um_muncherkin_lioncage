`default_nettype none

module tt_um_muncherkin_lioncage (
    input  wire [7:0] ui_in,    // Dedicated inputs - connected to the input switches
    output wire [7:0] uo_out,   // Dedicated outputs - connected to the 7 segment display
    input  wire [7:0] uio_in,   // IOs: Bidirectional Input path
    output wire [7:0] uio_out,  // IOs: Bidirectional Output path
    output wire [7:0] uio_oe,   // IOs: Bidirectional Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire reset = ! rst_n;
    wire [6:0] led_out;
    wire G_one = uio_in[2]; 
    wire G_two = uio_in[3];
    assign uo_out[6:0] = led_out;
    assign uo_out[7] = 0;

    // use bidirectionals as inputs
    assign uio_oe = 0;

    //Max 15 lions
    reg [3:0] lion_counter;
    reg state;

    always @(posedge clk) begin
        if (reset) begin
            lion_counter <= 0; 
            state <= 0;
        end else begin
            case(state)
            0: begin
                if (G_one) begin 
                   state <= 1;
                   if (! G_two) begin 
                    if(lion_counter == 15) begin
                        lion_counter <=0;
                    end else begin
                        lion_counter <= lion_counter + 1; 
                    end
                   end
                end
            end
            1: begin 
                if (! G_one) begin 
                   state <= 0;
                   if (! G_two) begin 
                    if(lion_counter == 0) begin
                        lion_counter <=15;
                    end else begin
                        lion_counter <= lion_counter - 1; 
                    end
                   end
                end
            end
            default:;
            endcase
        end
    end

    // instantiate segment display
    seg7 seg7(.counter(lion_counter), .segments(led_out));

endmodule
