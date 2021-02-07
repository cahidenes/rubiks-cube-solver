package main

import (
	"fmt"
	"io/ioutil"
	"time"
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

func rec(cube *Cube, depth int, last int) (string, bool) {
	if cube.isFinished() {
		return "", true
	}
	if depth == 0 {
		var f, s = findWhich(cube, 1)
		f()
		if cube.isFinished() {
			return s, true
		} else {
			f()
			f()
			f()
		}
		return "", false
	}
	depth--

	var sol string
	var bol bool

	if last != 1 {
		cube.U()
		sol, bol = rec(cube, depth, 1)
		if bol {
			return "U " + sol, true
		}
		cube.U()
		sol, bol = rec(cube, depth, 1)
		if bol {
			return "U2 " + sol, true
		}
		cube.U()
		sol, bol = rec(cube, depth, 1)
		if bol {
			return "U' " + sol, true
		}
		cube.U()
	}
	if last != 2 && last != 1 {
		cube.D()
		sol, bol = rec(cube, depth, 2)
		if bol {
			return "D " + sol, true
		}
		cube.D()
		sol, bol = rec(cube, depth, 2)
		if bol {
			return "D2 " + sol, true
		}
		cube.D()
		sol, bol = rec(cube, depth, 2)
		if bol {
			return "D' " + sol, true
		}
		cube.D()
	}

	if last != 3 {

		cube.R()
		sol, bol = rec(cube, depth, 3)
		if bol {
			return "R " + sol, true
		}
		cube.R()
		sol, bol = rec(cube, depth, 3)
		if bol {
			return "R2 " + sol, true
		}
		cube.R()
		sol, bol = rec(cube, depth, 3)
		if bol {
			return "R' " + sol, true
		}
		cube.R()
	}

	if last != 4 && last != 3 {

		cube.L()
		sol, bol = rec(cube, depth, 4)
		if bol {
			return "L " + sol, true
		}
		cube.L()
		sol, bol = rec(cube, depth, 4)
		if bol {
			return "L2 " + sol, true
		}
		cube.L()
		sol, bol = rec(cube, depth, 4)
		if bol {
			return "L' " + sol, true
		}
		cube.L()
	}

	if last != 5 {

		cube.F()
		sol, bol = rec(cube, depth, 5)
		if bol {
			return "F " + sol, true
		}
		cube.F()
		sol, bol = rec(cube, depth, 5)
		if bol {
			return "F2 " + sol, true
		}
		cube.F()
		sol, bol = rec(cube, depth, 5)
		if bol {
			return "F' " + sol, true
		}
		cube.F()

	}
	if last != 6 && last != 5 {

		cube.B()
		sol, bol = rec(cube, depth, 6)
		if bol {
			return "B " + sol, true
		}
		cube.B()
		sol, bol = rec(cube, depth, 6)
		if bol {
			return "B2 " + sol, true
		}
		cube.B()
		sol, bol = rec(cube, depth, 6)
		if bol {
			return "B' " + sol, true
		}
		cube.B()
	}

	return "", false

}

func doTest(cube *Cube, testNumber int) bool {
	if testNumber < 24*8 {
		return int(cube.corners[testNumber%8]) == testNumber/8
	}
	testNumber -= 24 * 8
	if testNumber < 24*12 {
		return int(cube.edges[testNumber%12]) == testNumber/12
	}
	panic("test limit (480) exceeded")
}

var l, l_size = [10000]Cube{}, 0
var l1, l1_size = [10000]Cube{}, 0
var l2, l2_size = [10000]Cube{}, 0

var r, r_size = [10000]Cube{}, 0
var r1, r1_size = [10000]Cube{}, 0
var r2, r2_size = [10000]Cube{}, 0

var u, u_size = [10000]Cube{}, 0
var u1, u1_size = [10000]Cube{}, 0
var u2, u2_size = [10000]Cube{}, 0

var d, d_size = [10000]Cube{}, 0
var d1, d1_size = [10000]Cube{}, 0
var d2, d2_size = [10000]Cube{}, 0

var f, f_size = [10000]Cube{}, 0
var f1, f1_size = [10000]Cube{}, 0
var f2, f2_size = [10000]Cube{}, 0

var b, b_size = [10000]Cube{}, 0
var b1, b1_size = [10000]Cube{}, 0
var b2, b2_size = [10000]Cube{}, 0

func rulesRec(cube Cube, depth int, last int, number int) {
	if depth == 0 {
		if last == 1 {
			if number == 1 {
				u1[u1_size] = cube
				u1_size++
			} else if number == 2 {
				u2[u2_size] = cube
				u2_size++
			} else {
				u[u_size] = cube
				u_size++
			}
		} else if last == 2 {
			if number == 1 {
				d1[d1_size] = cube
				d1_size++
			} else if number == 2 {
				d2[d2_size] = cube
				d2_size++
			} else {
				d[d_size] = cube
				d_size++
			}
		} else if last == 3 {
			if number == 1 {
				r1[r1_size] = cube
				r1_size++
			} else if number == 2 {
				r2[r2_size] = cube
				r2_size++
			} else {
				r[r_size] = cube
				r_size++
			}
		} else if last == 4 {
			if number == 1 {
				l1[l1_size] = cube
				l1_size++
			} else if number == 2 {
				l2[l2_size] = cube
				l2_size++
			} else {
				l[l_size] = cube
				l_size++
			}
		} else if last == 5 {
			if number == 1 {
				f1[f1_size] = cube
				f1_size++
			} else if number == 2 {
				f2[f2_size] = cube
				f2_size++
			} else {
				f[f_size] = cube
				f_size++
			}
		} else if last == 6 {
			if number == 1 {
				b1[b1_size] = cube
				b1_size++
			} else if number == 2 {
				b2[b2_size] = cube
				b2_size++
			} else {
				b[b_size] = cube
				b_size++
			}
		}
		return
	}
	depth--

	if last != 1 {
		cube.U()
		rulesRec(cube, depth, 1, 1)
		cube.U()
		rulesRec(cube, depth, 1, 2)
		cube.U()
		rulesRec(cube, depth, 1, 3)
		cube.U()
	}
	if last != 2 && last != 1 {
		cube.D()
		rulesRec(cube, depth, 2, 1)
		cube.D()
		rulesRec(cube, depth, 2, 2)
		cube.D()
		rulesRec(cube, depth, 2, 3)
		cube.D()
	}

	if last != 3 {

		cube.R()
		rulesRec(cube, depth, 3, 1)
		cube.R()
		rulesRec(cube, depth, 3, 2)
		cube.R()
		rulesRec(cube, depth, 3, 3)
		cube.R()
	}

	if last != 4 && last != 3 {

		cube.L()
		rulesRec(cube, depth, 4, 1)
		cube.L()
		rulesRec(cube, depth, 4, 2)
		cube.L()
		rulesRec(cube, depth, 4, 3)
		cube.L()
	}

	if last != 5 {

		cube.F()
		rulesRec(cube, depth, 5, 1)
		cube.F()
		rulesRec(cube, depth, 5, 2)
		cube.F()
		rulesRec(cube, depth, 5, 3)
		cube.F()

	}
	if last != 6 && last != 5 {

		cube.B()
		rulesRec(cube, depth, 6, 1)
		cube.B()
		rulesRec(cube, depth, 6, 2)
		cube.B()
		rulesRec(cube, depth, 6, 3)
		cube.B()
	}
}

// func findRules(level int) {
// 	var cube Cube
// 	for i := 0; i < 8; i++ {
// 		cube.corners[i] = byte(i)
// 	}
// 	for i := 0; i < 12; i++ {
// 		cube.edges[i] = byte(i)
// 	}
// 	rulesRec(cube, level, 0, 0)

// 	for i := 0; i < 480; i++ {
// 		var allCorrect = 0
// 		var allWrong = 0

// 		var listlist = [][10000]Cube{u, u1, u2, d, d1, d2, r, r1, r2, l, l1, l2, f, f1, f2, b, b1, b2}
// 		var sizelist = []int{u_size, u1_size, u2_size, d_size, d1_size, d2_size, r_size, r1_size, r2_size, l_size, l1_size, l2_size, f_size, f1_size, f2_size, b_size, b1_size, b2_size}

// 		// fmt.Printf("%d ", i)

// 		// var whichcorrect = -1

// 		for j := 0; j < 18; j++ {
// 			var allCorrectBool = true
// 			var allWrongBool = true
// 			for k := 0; k < sizelist[j]; k++ {
// 				if doTest(listlist[j][k], i) {
// 					allWrongBool = false
// 				} else {
// 					allCorrectBool = false
// 				}
// 			}
// 			if true {
// 				if allCorrectBool {
// 					allCorrect++
// 				} else if allWrongBool {
// 					allWrong++
// 				}
// 			}

// 			if allCorrectBool {
// 				fmt.Print("1")
// 				// whichcorrect = j
// 			} else if allWrongBool {
// 				fmt.Print("0")
// 			} else {
// 				fmt.Print("-")
// 			}
// 		}
// 		fmt.Println()

// 		// if allCorrect+allWrong == 18 {
// 		// 	if allCorrect == 1 {
// 		// 		fmt.Printf("---------- %d -------------!!!\n", whichcorrect)
// 		// 	}
// 		// }

// 	}

// }

// ---: 012345678901234567
// 0  : 000111111000000111
// 9  : 000111000111000111
// 18 : 000111000111111000
// 1  : 100000000000000000
// 3  : 010000000000000000
// 2  : 001000000000000000
// 39 : 000100000000000000
// 37 : 000010000000000000
// 38 : 000001000000000000
// 77 : 000000100000000000
// 74 : 000000010000000000
// 213: 000000001000000000
// 188: 000000000100000000
// 187: 000000000010000000
// 239: 000000000001000000
// 388: 000000000000100000
// 389: 000000000000010000
// 5  : 000000000000001000
// 414: 000000000000000100
// 415: 000000000000000010
// 23 : 000000000000000001

func findWhich(cube *Cube, level int) (func(), string) {
	if level == 1 {
		if doTest(cube, 63) == true {
			if doTest(cube, 309) == true {
				if doTest(cube, 296) == true {
					if doTest(cube, 230) == true {
						return cube.U1, "U1"
					} else {
						if doTest(cube, 229) == true {
							return cube.U2, "U2"
						} else {
							return cube.U, "U"
						}
					}
				} else {
					if doTest(cube, 452) == true {
						return cube.F1, "F1"
					} else {
						if doTest(cube, 444) == true {
							return cube.F, "F"
						} else {
							return cube.F2, "F2"
						}
					}
				}
			} else {
				if doTest(cube, 306) == true {
					return cube.R, "R"
				} else {
					if doTest(cube, 305) == true {
						return cube.R1, "R1"
					} else {
						return cube.R2, "R2"
					}
				}
			}
		} else {
			if doTest(cube, 335) == true {
				if doTest(cube, 478) == true {
					return cube.B1, "B1"
				} else {
					if doTest(cube, 470) == true {
						return cube.B, "B"
					} else {
						return cube.B2, "B2"
					}
				}
			} else {
				if doTest(cube, 322) == true {
					if doTest(cube, 331) == true {
						return cube.L1, "L1"
					} else {
						if doTest(cube, 328) == true {
							return cube.L, "L"
						} else {
							return cube.L2, "L2"
						}
					}
				} else {
					if doTest(cube, 334) == true {
						return cube.D, "D"
					} else {
						if doTest(cube, 333) == true {
							return cube.D2, "D2"
						} else {
							return cube.D1, "D1"
						}
					}
				}
			}
		}
	} else if level == 2 {

	} else if level == 3 {

	} else if level == 4 {

	}
	return nil, ""
}

func main() {
	var cubeList, _ = ioutil.ReadFile("in")
	var cube = makeCube(cubeList)

	var begin = time.Now()
	var solution, success = rec(&cube, 7, 0)
	fmt.Println(time.Since(begin))
	fmt.Println(success)
	fmt.Println(solution)

	// findRules(2)

	// cube.L()
	// var _, str = findWhich(cube)
	// fmt.Println(str)
}
