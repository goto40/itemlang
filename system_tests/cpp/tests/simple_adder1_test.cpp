#include "catch.hpp"
#include "algos/simple_adder1.h"

TEST_CASE( "simple_adder1 test (manual)", "[algo]" ) {

    project::example::Simple a,b,c;
    a.init(3);
    b.init(3);

    for (size_t k=0;k<a.n;k++) {
        a.a_ui16[k] = (k+1)*10;
        b.a_ui16[k] = (k+1)*100;
    }

    algos::simple_adder1(a,b,c);

    REQUIRE( c.n == 3 );
    REQUIRE( a.n == b.n );
    REQUIRE( a.n == c.n );

    for (size_t k=0;k<c.n;k++) {
        REQUIRE( c.a_ui16[k] == (k+1)*10 + (k+1)*100);
    }

}

TEST_CASE( "simple_adder1 execption test (manual)", "[algo]" ) {

    project::example::Simple a,b,c;
    a.init(3);
    b.init(4);

    for (size_t k=0;k<a.n;k++) {
        a.a_ui16[k] = (k+1)*10;
        b.a_ui16[k] = (k+1)*100;
    }

    REQUIRE_THROWS_AS(algos::simple_adder1(a,b,c), std::runtime_error);
}
