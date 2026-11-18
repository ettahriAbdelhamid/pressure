#include <fstream>
#include <iostream>

using namespace std;
#define PREC float

int main(int argc, char** argv)
{

    std::cout << argv[1] << "\n";
    std::cout << argv[2] << "\n";

    int64_t nssmall = 2;
    int64_t ntsmall = 2;
    int64_t nslarge = 4;
    int64_t ntlarge = 2;

    const int64_t entries = 3 * 2;
    const int64_t small_sites = nssmall * nssmall * nssmall * ntsmall;
    const int64_t large_sites = nslarge * nslarge * nslarge * ntlarge;
    const int64_t bytes_per_link = 2 * entries * sizeof(PREC);
    const int64_t expected_small_payload = small_sites * 4 * bytes_per_link;
    const int64_t expected_large_payload = large_sites * 4 * bytes_per_link;

    std::ifstream input( argv[1], std::ios::in | std::ios::binary );
    if (!input) {
        cerr << "Error: cannot open input file " << argv[1] << "\n";
        return 1;
    }

    input.seekg( 0, std::ios::end );
    int64_t filesize = input.tellg();
    if (filesize < expected_small_payload) {
        cerr << "Error: input file too small for a "
             << nssmall << "x" << nssmall << "x" << nssmall << "x" << ntsmall
             << " gauge field (expected at least " << expected_small_payload << " bytes, got " << filesize << ")\n";
        return 1;
    }

    cout << filesize <<  endl;

    int64_t header_length = filesize - expected_small_payload;

    cout << "Header length is "  << header_length << endl;

    input.seekg( 0, std::ios::beg );

    int64_t seekg_offset = 0; 

    std::fstream myfile;
    myfile = std::fstream(argv[2], std::ios::out | std::ios::binary);

    char matrix[2*entries*sizeof(PREC)];

    for ( int64_t i = 0; i < header_length; ++i ) {
        input.read( (char*)&matrix, 1 );
        myfile.write((char*)&matrix,1 );
    }
    //int64_t val1 = 20;
    //int64_t val2 = 6; 
    //cout << 20%6 << endl;
    //cout << val1%val2 << endl;
    //cout << 20%20 << endl;
    int64_t sum = 0;
    cout << 18*sizeof(PREC) << endl;

    for ( int64_t it = 0; it < ntlarge; ++it ) {
    for ( int64_t iz = 0; iz < nslarge; ++iz ) {
    for ( int64_t iy = 0; iy < nslarge; ++iy ) {
    for ( int64_t ix = 0; ix < nslarge; ++ix ) {
        for ( int imu = 0; imu < 4; ++imu ) {

            input.seekg( header_length + bytes_per_link * (imu + 4 * ((ix % nssmall) + nssmall * ((iy % nssmall) + nssmall * ((iz % nssmall) + nssmall * (it % ntsmall))))), std::ios::beg );
            sum += bytes_per_link;
            input.read( (char*)&matrix, bytes_per_link );
            myfile.write((char*)&matrix, bytes_per_link );
        }
    }}}}

    cout << "Wrote " << sum << " bytes; expected " << expected_large_payload << " bytes\n";
    if (sum != expected_large_payload) {
        cerr << "Error: grown lattice payload has incorrect size. Check the lattice mapping or the file format.\n";
        input.close();
        myfile.close();
        return 1;
    }

    input.close();
    myfile.close();
    return 0;
}


