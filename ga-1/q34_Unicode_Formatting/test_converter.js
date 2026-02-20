const { convertToMarkdown } = require('./converter');

const tests = [
    {
        name: "Bold text",
        input: "𝗕𝗼𝗹𝗱 𝘁𝗲𝘅𝘁",
        expected: "**Bold text**"
    },
    {
        name: "Italic text",
        input: "𝘐𝘵𝘢𝘭𝘪𝘤 𝘵𝘦𝘹𝘵",
        expected: "*Italic text*"
    },
    {
        name: "Inline code",
        input: "𝚌𝚘𝚍𝚎()",
        expected: "`code()`"
    },
    {
        name: "Mixed bold and italic",
        input: "𝗕𝗼𝗹𝗱 and 𝘐𝘵𝘢𝘭𝘪𝘤",
        expected: "**Bold** and *Italic*"
    },
    {
        name: "Bullet list",
        input: "• Item 1\n• Item 2",
        expected: "- Item 1\n- Item 2"
    },
    {
        name: "Multi-line code block",
        input: "𝚏𝚞𝚗𝚌 𝚖𝚊𝚒𝚗()\n𝚏𝚞𝚗𝚌 𝚝𝚎𝚜𝚝()\n𝚏𝚞𝚗𝚌 𝚑𝚎𝚕𝚕𝚘()",
        expected: "```\nfunc main()\nfunc test()\nfunc hello()\n```"
    },
    {
        name: "Complex document",
        input: "• 𝗕𝗼𝗹𝗱 𝘁𝗶𝘁𝗹𝗲\n\n𝘐𝘵𝘢𝘭𝘪𝘤 𝘥𝘦𝘴𝘤𝘳𝘪𝘱𝘵𝘪𝘰𝘯\n\n• 𝙰𝙱𝙲_𝟷𝟸𝟹\n• 𝙳𝙴𝙵_𝟺𝟻𝟼\n• 𝙶𝙷𝙸_𝟽𝟾𝟿",
        expected: "- **Bold title**\n\n*Italic description*\n\n```\nABC_123\nDEF_456\nGHI_789\n```"
    },
    {
        name: "Code with numbers",
        input: "𝚟𝚊𝚛 𝚡 = 𝟷𝟶",
        expected: "`var x = 10`"
    }
];

let allPassed = true;
tests.forEach(test => {
    const output = convertToMarkdown(test.input);
    if (output === test.expected) {
        console.log(`✅ PASS: ${test.name}`);
    } else {
        console.log(`❌ FAIL: ${test.name}`);
        console.log(`   Input:    ${JSON.stringify(test.input)}`);
        console.log(`   Expected: ${JSON.stringify(test.expected)}`);
        console.log(`   Got:      ${JSON.stringify(output)}`);
        allPassed = false;
    }
});

if (!allPassed) process.exit(1);
