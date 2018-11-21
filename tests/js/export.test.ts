import "isomorphic-fetch";

import * as extension from '../../ts/src/index';

describe('Checks exports', () => {
  test("Check extension", () => {
     expect(extension);
  });
});
