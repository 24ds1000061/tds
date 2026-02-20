function convertToMarkdown(text) {
    const BULLETS = ["•", "◦", "▪", "▸", "‣"];

    const ranges = {
        bold: [
            [0x1D5D4, 0x1D5ED, 'A'.charCodeAt(0)], // ABC (Sans)
            [0x1D5EE, 0x1D607, 'a'.charCodeAt(0)], // abc (Sans)
            [0x1D7EC, 0x1D7F5, '0'.charCodeAt(0)], // 012 (Sans)
            [0x1D400, 0x1D419, 'A'.charCodeAt(0)], // ABC (Serif)
            [0x1D41A, 0x1D433, 'a'.charCodeAt(0)], // abc (Serif)
            [0x1D7CE, 0x1D7D7, '0'.charCodeAt(0)], // 012 (Serif)
        ],
        italic: [
            [0x1D608, 0x1D621, 'A'.charCodeAt(0)], // ABC (Sans)
            [0x1D622, 0x1D63B, 'a'.charCodeAt(0)], // abc (Sans)
            [0x1D434, 0x1D44D, 'A'.charCodeAt(0)], // ABC (Serif)
            [0x1D44E, 0x1D467, 'a'.charCodeAt(0)], // abc (Serif)
        ],
        mono: [
            [0x1D670, 0x1D689, 'A'.charCodeAt(0)], // ABC
            [0x1D68A, 0x1D6A3, 'a'.charCodeAt(0)], // abc
            [0x1D7F6, 0x1D7FF, '0'.charCodeAt(0)], // 012
        ]
    };

    const mapChar = (char) => {
        const cp = char.codePointAt(0);
        for (const [style, styleRanges] of Object.entries(ranges)) {
            for (const [start, end, base] of styleRanges) {
                if (cp >= start && cp <= end) {
                    return { char: String.fromCharCode(base + (cp - start)), style };
                }
            }
        }
        return { char, style: null };
    };

    const mapText = (t) => {
        let result = "";
        for (const char of t) {
            result += mapChar(char).char;
        }
        return result;
    };

    const convertInline = (line) => {
        let chars = [...line];
        let output = "";
        let i = 0;
        while (i < chars.length) {
            let { style, char: normalChar } = mapChar(chars[i]);
            if (style) {
                let span = normalChar;
                let j = i + 1;
                while (j < chars.length) {
                    let { style: nextStyle, char: nextNormal } = mapChar(chars[j]);
                    if (nextStyle === style) {
                        span += nextNormal;
                        j++;
                    } else if (chars[j] === " " || chars[j] === "\t") {
                        let k = j + 1;
                        while (k < chars.length && (chars[k] === " " || chars[k] === "\t")) k++;
                        if (k < chars.length && mapChar(chars[k]).style === style) {
                            span += chars.slice(j, k).join("");
                            j = k;
                        } else {
                            break;
                        }
                    } else {
                        break;
                    }
                }
                if (style === 'bold') output += `**${span}**`;
                else if (style === 'italic') output += `*${span}*`;
                else if (style === 'mono') output += `\`${span}\``;
                i = j;
            } else {
                output += chars[i];
                i++;
            }
        }
        return output;
    };

    const isMonoLine = (line) => {
        let hasMono = false;
        let hasOtherAlphaNum = false;
        for (const char of line) {
            const { style, char: normalChar } = mapChar(char);
            if (style === 'mono') {
                hasMono = true;
            } else if (/[a-zA-Z0-9]/.test(normalChar)) {
                hasOtherAlphaNum = true;
            }
        }
        return hasMono && !hasOtherAlphaNum;
    };

    let lines = text.split("\n");
    lines = lines.map(line => {
        let trimmed = line.trimStart();
        if (trimmed.length > 0 && BULLETS.includes(trimmed[0])) {
            return line.replace(trimmed[0], "-");
        }
        return line;
    });

    const monoStatus = lines.map(isMonoLine);
    let resultLines = [];
    for (let i = 0; i < lines.length; i++) {
        let count = 0;
        while (i + count < lines.length && monoStatus[i + count]) {
            count++;
        }

        if (count >= 3) {
            resultLines.push("```");
            for (let j = 0; j < count; j++) {
                resultLines.push(mapText(lines[i + j]));
            }
            resultLines.push("```");
            i += count - 1;
        } else {
            resultLines.push(convertInline(lines[i]));
        }
    }

    return resultLines.join("\n");
}

module.exports = { convertToMarkdown };
