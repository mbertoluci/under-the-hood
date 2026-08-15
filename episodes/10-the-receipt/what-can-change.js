/**
 * Your package.json is a wish. The lockfile is a receipt.
 *
 * "express": "^4.16.0" doesn't name a version. It names a RANGE, and
 * every fresh install without a lockfile is free to pick any version
 * inside it. This script asks the npm registry how many versions your
 * innocent-looking range actually allows today.
 *
 * Run:
 *   node episodes/10-the-receipt/what-can-change.js
 */

import { execSync } from 'node:child_process';

const dep = 'express';
const range = '^4.16.0';

const versions = JSON.parse(
  execSync(`npm view "${dep}@${range}" version --json`, { encoding: 'utf8' })
);

console.log(`package.json says:   "${dep}": "${range}"`);
console.log(`versions that satisfy that range today: ${versions.length}`);
console.log(`oldest: ${versions[0]}   newest: ${versions.at(-1)}`);
console.log();
console.log('Without a lockfile, a fresh install may legally pick any of them.');
console.log('The lockfile writes down the ONE combination you actually tested.');
