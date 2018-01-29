package data {
    type int {}
    type float  {}
    struct Data {
        scalar n: int { default="10" }
        array a: float[n]
    }
}
