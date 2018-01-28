#include "catch.hpp"
#include "project/example/Simple.h"
#include "attributes/tools.h"
#include <sstream>

TEST_CASE( "Simple", "[io]" ) {

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

