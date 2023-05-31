#include <iostream>

#include "placement.cc"

int main(int argc, char** argv) {
	if (argc != 2) {
		std::cerr << "Requires one argument (netlist filename)." << std::endl;
		return 1;
	}
	Netlist netlist = Netlist::from_file(argv[1]);
	Placement initial = Placement::from_netlist_naive(netlist, 20, 20);
	std::cout << initial.text_all() << std::endl;
	return 0;
}

