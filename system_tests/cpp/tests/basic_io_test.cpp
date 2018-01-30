#include "catch.hpp"
#include "project/example/Simple.h"
#include "attributes/tools.h"
#include <sstream>
#include <fstream>

TEST_CASE( "Simple.pprint", "[io]" ) {

    project::example::Simple simple;
    simple.init(3);

    for (size_t k=0;k<simple.n;k++) {
        simple.a_ui16[k] = (k+1)*10;
    }

    std::stringstream s;    
    attributes::tools::pprint(simple, s);

    REQUIRE( s.str() == R"(Simple {
  UINT16 n = 3
  UINT16 x = 0
  UINT16[] a_ui16 = [ 10 20 30 ]
}
)");
}

TEST_CASE( "Simple.binary_read_write", "[io]" ) {

    project::example::Simple simple1;
    simple1.init(9);
    for (size_t k=0;k<simple1.n;k++) {
        simple1.a_ui16[k] = (k+1)*10;
    }
    { // write
        std::ofstream fo("data.bin");    
        attributes::tools::binary_write(simple1, fo);
    }

    project::example::Simple simple2;
    { // read
        std::ifstream fi("data.bin");    
        attributes::tools::binary_read(simple2, fi);
    }

    // compare
    REQUIRE(simple2.n == simple1.n);
    for (size_t k=0;k<simple2.n;k++) {
        REQUIRE(simple2.a_ui16[k] == (k+1)*10);
    }    
}

