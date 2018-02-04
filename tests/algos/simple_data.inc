package data {
    type int as custom {}
    type float as custom {}
    struct Data {
        scalar n: int { default="10" }
        array a: float[n]
    }
}
