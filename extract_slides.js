const fs = require('fs');
const path = require('path');

const filePath = '/Users/mw/Sites/LIFEGENIX LOBBY SCREEENS/index.html';
const content = fs.readFileSync(filePath, 'utf8');

const startMarker = 'const SLIDES = ';
const startIndex = content.indexOf(startMarker);

if (startIndex !== -1) {
    let bracketCount = 0;
    let endIndex = -1;
    for (let i = startIndex + startMarker.length; i < content.length; i++) {
        if (content[i] === '[') bracketCount++;
        if (content[i] === ']') bracketCount--;
        if (bracketCount === 0 && endIndex === -1 && i > startIndex + startMarker.length) {
            endIndex = i + 1;
            break;
        }
    }

    if (endIndex !== -1) {
        const slidesJson = content.substring(startIndex + startMarker.length, endIndex);
        try {
            const slides = JSON.parse(slidesJson);
            fs.writeFileSync('/Users/mw/Sites/LIFEGENIX LOBBY SCREEENS/slides.json', JSON.stringify(slides, null, 2));
            console.log('Successfully extracted SLIDES to slides.json');
        } catch (e) {
            console.error('Failed to parse SLIDES JSON:', e);
            // Fallback: just write the raw string if parsing fails (maybe it's not pure JSON yet)
            fs.writeFileSync('/Users/mw/Sites/LIFEGENIX LOBBY SCREEENS/slides.json', slidesJson);
            console.log('Wrote raw SLIDES content to slides.json (failed to parse as JSON)');
        }
    } else {
        console.error('Could not find end of SLIDES array');
    }
} else {
    console.error('Could not find SLIDES array start');
}
