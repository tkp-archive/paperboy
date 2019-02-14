import "isomorphic-fetch";

import * as extension from '../../src/ts/index';

describe('Checks exports', () => {
  test("Check extension", () => {
     expect(extension);
  });
});
