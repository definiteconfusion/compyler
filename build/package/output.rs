fn main() {
/*4*/
let k = 15;
/*8*/
let mut evenInts = vec![];
/*36*/
for i in 0..k {
/*56*/
if i % 2 == 0 {
/*78*/
evenInts.push(i);
}
}
/*104*/
println!("{:?}", evenInts);
}
