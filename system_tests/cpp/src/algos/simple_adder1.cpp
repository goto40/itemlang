#include "algos/simple_adder1.h" 
#include <stdexcept>

namespace algos {
    void simple_adder1(const project::example::Simple& a,
                       const project::example::Simple& b,
                             project::example::Simple& c)
    {
        if(a.n != b.n) {
            throw std::runtime_error("a and b have not the same size");
        }
        c.init(a.n);
        for (size_t i=0;i<a.n;i++)
        {
            c.a_ui16[i] = a.a_ui16[i]+b.a_ui16[i];
        }
    }
}
