fn main() {
let mut t = 1;
let mut tx = 1;
let mut _x = ("test", "words");
for k in 0..10 {
t = tx;
tx = t + tx;
println!("{:?}", tx);
}
}
