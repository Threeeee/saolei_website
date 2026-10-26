import { readFileSync } from 'node:fs';

import { describe, expect, it } from 'vitest';

import { MedalDirection, MedalKind, MedalSeries, MedalStyle } from './medal_const';

describe('medal wire enums', () => {
    it('matches backend choices without case-insensitive collisions', () => {
        const source = readFileSync(new URL('../../../back_end/saolei/config/text_choices.py', import.meta.url), 'utf8');
        const [, medalChoices] = source.split('class Medal_TextChoices:');
        const groups: Record<string, Readonly<Record<string, string>>> = { Series: MedalSeries, Kind: MedalKind, Direction: MedalDirection, Style: MedalStyle };
        for (const [name, values] of Object.entries(groups)) {
            const [, definition] = medalChoices.split(`class ${name}(TextChoices):`);
            const [block] = definition.split(/\n {4}class |\nclass /);
            const pairs = [...block.matchAll(/^ {8}([A-Z_]+) = '([^']+)'/gm)].map((match) => [match[1], match[2]]);
            expect(values).toEqual(Object.fromEntries(pairs));
            const codes = Object.values(values);
            expect(new Set(codes.map((code) => code.toLowerCase())).size).toBe(codes.length);
            expect(codes.every((code) => code.length <= (name === 'Series' ? 2 : 1))).toBe(true);
        }
    });
});
