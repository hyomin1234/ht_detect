module top (
    input A,
    input B,
    output Z
);
wire w1;
AND2_X1 u1 (.A(A), .B(B), .Z(w1)); // Driver w1
INV_X1 u2 (.A(w1), .Z(Z));         // Load w1, Driver Z
endmodule
