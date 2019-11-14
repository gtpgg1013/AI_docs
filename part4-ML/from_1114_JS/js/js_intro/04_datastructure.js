// 04_datastructure.js

// 1. 배열
const numbers = [1,2,3,4]

numbers[0] // 1
numbers[-1] // undefined => 정확한 양의 정수만 index 가능!
numbers.length


// 원본 파괴
numbers.reverse()
numbers // [4,3,2,1]

// push - 배열의 길이 return
numbers.push('a') // 5
numbers // [1,2,3,4,'a']

// pop - 배열의 가장 마지막 요소 제거 후 return
numbers.pop()

// unshift - 배열의 가장 앞에 요소 추가
numbers.unshift('a') // 5
numbers // ['a',1,2,3,4]

// shift - 배열의 가장 첫번째 요소 제거 후 return
numbers.shift() // 'a'
numbers // [1,2,3,4]

numbers.includes(1) // true
numbers.includes(0) // false

numbers.push(4)
numbers // [1,2,3,4,4]
numbers.indexOf(4) // 3 => 중복이 존재한다면 처음 찾은 요소의 index 반환
numbers.indexOf('c') // -1 => 없으면 -1

// join - 배열의 요소를 join 함수의 인자를 기준으로 이어서 문자열 return
numbers.join() // 아무것도 넣지 않으면 ','를 기준으로 가져옴 '1,2,3,4,4'
numbers.join('') // 12344