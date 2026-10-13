fn main() {
/*4*/
let mut evenInts = vec![];
/*8*/
let mut exs = 0;
/*12*/
let rg = 10;
/*40*/
for i in 0..rg {
/*60*/
if i % 2 == 0 {
/*82*/
evenInts.push(i);
}
}
/*106*/
for k in evenInts.iter() {
/*132*/
if k + 5 / 2 > 1 {
/*140*/
exs += 1;
}
}
/*156*/
println!("{:?}", exs);
}
