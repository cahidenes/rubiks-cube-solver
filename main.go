package main

import (
	"fmt"
	"io/ioutil"
)

// Cube Küpün kendisi
type Cube struct {
	corners [8]byte  // ilk 3 bit tip, sonraki 2 bit orient
	edges   [12]byte // ilk 4 bit tip, sonraki 1 bit orient
}

func (cube Cube) String() string {
	return fmt.Sprint("corners: \n", cube.corners, "\nedges: \n", cube.edges)
}

var cornerTable = map[byte]byte{
	0b010101: 0,
	0b100101: 1,
	0b101001: 2,
	0b011001: 3,
	0b010110: 4,
	0b100110: 5,
	0b101010: 6,
	0b011010: 7,
}

var edgeTable = map[byte]byte{
	0b000101: 0,
	0b100001: 1,
	0b001001: 2,
	0b010001: 3,
	0b010100: 4,
	0b100100: 5,
	0b101000: 6,
	0b011000: 7,
	0b000110: 8,
	0b100010: 9,
	0b001010: 10,
	0b010010: 11,
}

func makeCube(cubeList []byte) Cube {
	var ret Cube
	for i := range cubeList {
		if cubeList[i] == byte('W') {
			cubeList[i] = 1 << 0
		} else if cubeList[i] == byte('Y') {
			cubeList[i] = 1 << 1
		} else if cubeList[i] == byte('O') {
			cubeList[i] = 1 << 2
		} else if cubeList[i] == byte('R') {
			cubeList[i] = 1 << 3
		} else if cubeList[i] == byte('B') {
			cubeList[i] = 1 << 4
		} else if cubeList[i] == byte('G') {
			cubeList[i] = 1 << 5
		}
	}

	/*
		          0  1  2
		          4  5  6
		          8  9  10
		12 13 14  15 16 17  18 19 20  21 22 23
		25 26 27  28 29 30  31 32 33  34 35 36
		38 39 40  41 42 43  44 45 46  47 48 49
				  51 52 53
				  55 56 57
				  59 60 61

	*/

	ret.edges[0] = edgeTable[cubeList[9]+cubeList[16]]
	ret.edges[1] = edgeTable[cubeList[6]+cubeList[19]]
	ret.edges[2] = edgeTable[cubeList[1]+cubeList[22]]
	ret.edges[3] = edgeTable[cubeList[4]+cubeList[13]]
	ret.edges[4] = edgeTable[cubeList[27]+cubeList[28]]
	ret.edges[5] = edgeTable[cubeList[30]+cubeList[31]]
	ret.edges[6] = edgeTable[cubeList[33]+cubeList[34]]
	ret.edges[7] = edgeTable[cubeList[36]+cubeList[25]]
	ret.edges[8] = edgeTable[cubeList[52]+cubeList[42]]
	ret.edges[9] = edgeTable[cubeList[57]+cubeList[45]]
	ret.edges[10] = edgeTable[cubeList[60]+cubeList[48]]
	ret.edges[11] = edgeTable[cubeList[55]+cubeList[39]]

	ret.corners[0] = cornerTable[cubeList[8]+cubeList[14]+cubeList[15]]
	ret.corners[1] = cornerTable[cubeList[10]+cubeList[17]+cubeList[18]]
	ret.corners[2] = cornerTable[cubeList[2]+cubeList[20]+cubeList[21]]
	ret.corners[3] = cornerTable[cubeList[0]+cubeList[23]+cubeList[12]]
	ret.corners[4] = cornerTable[cubeList[40]+cubeList[41]+cubeList[51]]
	ret.corners[5] = cornerTable[cubeList[43]+cubeList[44]+cubeList[53]]
	ret.corners[6] = cornerTable[cubeList[46]+cubeList[47]+cubeList[61]]
	ret.corners[7] = cornerTable[cubeList[38]+cubeList[49]+cubeList[59]]

	if cubeList[9] > cubeList[16] {
		ret.edges[0] += 1 << 4
	}

	if cubeList[6] > cubeList[19] {
		ret.edges[1] += 1 << 4
	}

	if cubeList[1] > cubeList[22] {
		ret.edges[2] += 1 << 4
	}

	if cubeList[4] > cubeList[13] {
		ret.edges[3] += 1 << 4
	}

	if cubeList[28] > cubeList[27] {
		ret.edges[4] += 1 << 4
	}

	if cubeList[30] > cubeList[31] {
		ret.edges[5] += 1 << 4
	}

	if cubeList[34] > cubeList[33] {
		ret.edges[6] += 1 << 4
	}

	if cubeList[36] > cubeList[25] {
		ret.edges[7] += 1 << 4
	}

	if cubeList[52] > cubeList[42] {
		ret.edges[8] += 1 << 4
	}

	if cubeList[57] > cubeList[45] {
		ret.edges[9] += 1 << 4
	}

	if cubeList[60] > cubeList[48] {
		ret.edges[10] += 1 << 4
	}

	if cubeList[55] > cubeList[39] {
		ret.edges[11] += 1 << 4
	}

	if cubeList[8] < 3 {
		ret.corners[0] += 0 << 3
	} else if cubeList[15] < 3 {
		ret.corners[0] += 1 << 3
	} else {
		ret.corners[0] += 2 << 3
	}

	if cubeList[10] < 3 {
		ret.corners[1] += 0 << 3
	} else if cubeList[18] < 3 {
		ret.corners[1] += 1 << 3
	} else {
		ret.corners[1] += 2 << 3
	}

	if cubeList[2] < 3 {
		ret.corners[2] += 0 << 3
	} else if cubeList[21] < 3 {
		ret.corners[2] += 1 << 3
	} else {
		ret.corners[2] += 2 << 3
	}

	if cubeList[0] < 3 {
		ret.corners[3] += 0 << 3
	} else if cubeList[12] < 3 {
		ret.corners[3] += 1 << 3
	} else {
		ret.corners[3] += 2 << 3
	}

	if cubeList[51] < 3 {
		ret.corners[4] += 0 << 3
	} else if cubeList[40] < 3 {
		ret.corners[4] += 1 << 3
	} else {
		ret.corners[4] += 2 << 3
	}

	if cubeList[53] < 3 {
		ret.corners[5] += 0 << 3
	} else if cubeList[43] < 3 {
		ret.corners[5] += 1 << 3
	} else {
		ret.corners[5] += 2 << 3
	}

	if cubeList[61] < 3 {
		ret.corners[6] += 0 << 3
	} else if cubeList[46] < 3 {
		ret.corners[6] += 1 << 3
	} else {
		ret.corners[6] += 2 << 3
	}

	if cubeList[59] < 3 {
		ret.corners[7] += 0 << 3
	} else if cubeList[49] < 3 {
		ret.corners[7] += 1 << 3
	} else {
		ret.corners[7] += 2 << 3
	}

	return ret
}

func (cube *Cube) isFinished() bool {
	for i, corner := range cube.corners {
		if corner != byte(i) {
			return false
		}
	}

	for i, edge := range cube.edges {
		if edge != byte(i) {
			return false
		}
	}
	return true
}

func rotate(list []byte, a, b, c, d int) {
	list[a], list[b], list[c], list[d] = list[d], list[a], list[b], list[c]
}

func rrotate(list []byte, a, b, c, d int) {
	list[a], list[b], list[c], list[d] = list[b], list[c], list[d], list[a]
}

func swap(list []byte, a, b int) {
	list[a], list[b] = list[b], list[a]
}

func (cube *Cube) R() {
	rotate(cube.corners[:], 1, 2, 6, 5)
	rotate(cube.edges[:], 6, 9, 5, 1)
	cube.corners[1] = ((cube.corners[1]>>3+2)%3)<<3 + cube.corners[1]&0b111
	cube.corners[2] = ((cube.corners[2]>>3+1)%3)<<3 + cube.corners[2]&0b111
	cube.corners[5] = ((cube.corners[5]>>3+1)%3)<<3 + cube.corners[5]&0b111
	cube.corners[6] = ((cube.corners[6]>>3+2)%3)<<3 + cube.corners[6]&0b111
}

func (cube *Cube) R1() {
	rrotate(cube.corners[:], 1, 2, 6, 5)
	rrotate(cube.edges[:], 6, 9, 5, 1)
	cube.corners[1] = ((cube.corners[1]>>3+2)%3)<<3 + cube.corners[1]&0b111
	cube.corners[2] = ((cube.corners[2]>>3+1)%3)<<3 + cube.corners[2]&0b111
	cube.corners[5] = ((cube.corners[5]>>3+1)%3)<<3 + cube.corners[5]&0b111
	cube.corners[6] = ((cube.corners[6]>>3+2)%3)<<3 + cube.corners[6]&0b111
}

func (cube *Cube) R2() {
	swap(cube.corners[:], 1, 6)
	swap(cube.corners[:], 2, 5)
	swap(cube.edges[:], 5, 6)
	swap(cube.edges[:], 1, 9)
}

func (cube *Cube) L() {
	rotate(cube.corners[:], 0, 4, 7, 3)
	rotate(cube.edges[:], 3, 4, 11, 7)
	cube.corners[0] = ((cube.corners[0]>>3+1)%3)<<3 + cube.corners[0]&0b111
	cube.corners[4] = ((cube.corners[4]>>3+2)%3)<<3 + cube.corners[4]&0b111
	cube.corners[7] = ((cube.corners[7]>>3+1)%3)<<3 + cube.corners[7]&0b111
	cube.corners[3] = ((cube.corners[3]>>3+2)%3)<<3 + cube.corners[3]&0b111
}

func (cube *Cube) L1() {
	rrotate(cube.corners[:], 0, 4, 7, 3)
	rrotate(cube.edges[:], 3, 4, 11, 7)
	cube.corners[0] = ((cube.corners[0]>>3+1)%3)<<3 + cube.corners[0]&0b111
	cube.corners[4] = ((cube.corners[4]>>3+2)%3)<<3 + cube.corners[4]&0b111
	cube.corners[7] = ((cube.corners[7]>>3+1)%3)<<3 + cube.corners[7]&0b111
	cube.corners[3] = ((cube.corners[3]>>3+2)%3)<<3 + cube.corners[3]&0b111
}

func (cube *Cube) L2() {
	swap(cube.corners[:], 3, 4)
	swap(cube.corners[:], 0, 7)
	swap(cube.edges[:], 3, 11)
	swap(cube.edges[:], 4, 7)
}

func (cube *Cube) U() {
	rotate(cube.corners[:], 3, 2, 1, 0)
	rotate(cube.edges[:], 3, 2, 1, 0)
}

func (cube *Cube) U1() {
	rrotate(cube.corners[:], 3, 2, 1, 0)
	rrotate(cube.edges[:], 3, 2, 1, 0)
}

func (cube *Cube) U2() {
	swap(cube.corners[:], 0, 2)
	swap(cube.corners[:], 1, 3)
	swap(cube.edges[:], 0, 2)
	swap(cube.edges[:], 1, 3)
}

func (cube *Cube) D() {
	rotate(cube.corners[:], 4, 5, 6, 7)
	rotate(cube.edges[:], 8, 9, 10, 11)
}

func (cube *Cube) D1() {
	rrotate(cube.corners[:], 4, 5, 6, 7)
	rrotate(cube.edges[:], 8, 9, 10, 11)
}

func (cube *Cube) D2() {
	swap(cube.corners[:], 4, 6)
	swap(cube.corners[:], 5, 7)
	swap(cube.edges[:], 8, 10)
	swap(cube.edges[:], 9, 11)
}

func (cube *Cube) F() {
	rotate(cube.corners[:], 0, 1, 5, 4)
	rotate(cube.edges[:], 0, 5, 8, 4)

	cube.corners[0] = ((cube.corners[0]>>3+2)%3)<<3 + cube.corners[0]&0b111
	cube.corners[1] = ((cube.corners[1]>>3+1)%3)<<3 + cube.corners[1]&0b111
	cube.corners[5] = ((cube.corners[5]>>3+2)%3)<<3 + cube.corners[5]&0b111
	cube.corners[4] = ((cube.corners[4]>>3+1)%3)<<3 + cube.corners[4]&0b111

	cube.edges[0] ^= 1 << 4
	cube.edges[5] ^= 1 << 4
	cube.edges[8] ^= 1 << 4
	cube.edges[4] ^= 1 << 4
}

func (cube *Cube) F1() {
	rrotate(cube.corners[:], 0, 1, 5, 4)
	rrotate(cube.edges[:], 0, 5, 8, 4)

	cube.corners[0] = ((cube.corners[0]>>3+2)%3)<<3 + cube.corners[0]&0b111
	cube.corners[1] = ((cube.corners[1]>>3+1)%3)<<3 + cube.corners[1]&0b111
	cube.corners[5] = ((cube.corners[5]>>3+2)%3)<<3 + cube.corners[5]&0b111
	cube.corners[4] = ((cube.corners[4]>>3+1)%3)<<3 + cube.corners[4]&0b111

	cube.edges[0] ^= 1 << 4
	cube.edges[5] ^= 1 << 4
	cube.edges[8] ^= 1 << 4
	cube.edges[4] ^= 1 << 4
}

func (cube *Cube) F2() {
	swap(cube.corners[:], 0, 5)
	swap(cube.corners[:], 1, 4)
	swap(cube.edges[:], 0, 8)
	swap(cube.edges[:], 5, 4)
}

func (cube *Cube) B() {
	rotate(cube.corners[:], 2, 3, 7, 6)
	rotate(cube.edges[:], 2, 7, 10, 6)

	cube.corners[2] = ((cube.corners[2]>>3+2)%3)<<3 + cube.corners[2]&0b111
	cube.corners[3] = ((cube.corners[3]>>3+1)%3)<<3 + cube.corners[3]&0b111
	cube.corners[7] = ((cube.corners[7]>>3+2)%3)<<3 + cube.corners[7]&0b111
	cube.corners[6] = ((cube.corners[6]>>3+1)%3)<<3 + cube.corners[6]&0b111

	cube.edges[2] ^= 1 << 4
	cube.edges[7] ^= 1 << 4
	cube.edges[10] ^= 1 << 4
	cube.edges[6] ^= 1 << 4
}

func (cube *Cube) B1() {
	rrotate(cube.corners[:], 2, 3, 7, 6)
	rrotate(cube.edges[:], 2, 7, 10, 6)

	cube.corners[2] = ((cube.corners[2]>>3+2)%3)<<3 + cube.corners[2]&0b111
	cube.corners[3] = ((cube.corners[3]>>3+1)%3)<<3 + cube.corners[3]&0b111
	cube.corners[7] = ((cube.corners[7]>>3+2)%3)<<3 + cube.corners[7]&0b111
	cube.corners[6] = ((cube.corners[6]>>3+1)%3)<<3 + cube.corners[6]&0b111

	cube.edges[2] ^= 1 << 4
	cube.edges[7] ^= 1 << 4
	cube.edges[10] ^= 1 << 4
	cube.edges[6] ^= 1 << 4
}

func (cube *Cube) B2() {
	swap(cube.corners[:], 2, 7)
	swap(cube.corners[:], 3, 6)
	swap(cube.edges[:], 2, 10)
	swap(cube.edges[:], 7, 6)
}

func main() {
	var cubeList, _ = ioutil.ReadFile("in")
	var cube = makeCube(cubeList)
	fmt.Println(cube)
	cube.R1()
	cube.U1()
	cube.L()
	cube.D2()
	cube.U1()
	cube.L2()
	cube.B2()
	cube.L1()
	cube.D1()
	cube.F2()
	cube.D2()
	cube.U1()
	cube.L2()
	cube.R2()
	cube.D()
	cube.F1()
	cube.L()
	cube.B2()
	cube.D1()
	cube.F()

	fmt.Println(cube.isFinished())
	fmt.Println(cube)
}
