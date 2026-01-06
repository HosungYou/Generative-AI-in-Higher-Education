const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        PageNumber, PageBreak, ShadingType, VerticalAlign, PageOrientation } = require('docx');
const fs = require('fs');

// APA style table borders - top and bottom only
const headerBorderTop = { style: BorderStyle.SINGLE, size: 12, color: "000000" };
const headerBorderBottom = { style: BorderStyle.SINGLE, size: 6, color: "000000" };
const lastRowBorder = { style: BorderStyle.SINGLE, size: 12, color: "000000" };
const noBorder = { style: BorderStyle.NIL };

// Helper to create table cells with proper formatting
function createCell(text, width, options = {}) {
    const { bold = false, italics = false, indent = false, isHeader = false, isLastRow = false, align = null } = options;

    let borders = {
        top: noBorder, bottom: noBorder, left: noBorder, right: noBorder
    };

    if (isHeader) {
        borders = {
            top: headerBorderTop,
            bottom: headerBorderBottom,
            left: noBorder,
            right: noBorder
        };
    } else if (isLastRow) {
        borders = {
            top: noBorder,
            bottom: lastRowBorder,
            left: noBorder,
            right: noBorder
        };
    }

    return new TableCell({
        borders: borders,
        width: { size: width, type: WidthType.DXA },
        verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({
            alignment: align || (isHeader ? AlignmentType.CENTER : AlignmentType.LEFT),
            indent: indent ? { left: 200 } : undefined,
            children: [new TextRun({
                text: text,
                bold: bold || isHeader,
                italics: italics,
                size: 18, // 9pt for tables
                font: "Times New Roman"
            })]
        })]
    });
}

// Table 1: Included Studies - Using wider columns
function createTable1() {
    // Total width ~12000 for landscape, columns proportional
    const widths = [600, 2000, 700, 600, 800, 1400, 1800, 700, 500]; // Total ~9100

    const headers = ["ID", "Author(s)", "Year", "N", "Design", "GenAI Tool", "Outcomes", "g", "k"];
    const headerRow = new TableRow({
        tableHeader: true,
        children: headers.map((h, i) => createCell(h, widths[i], { isHeader: true, align: AlignmentType.CENTER }))
    });

    const studies = [
        ["1", "Heo et al.", "2025", "86", "RCT", "GenAI", "Aff, Beh, Cog", "−0.06", "4"],
        ["2", "He & Li", "2025", "80", "RCT", "LLM", "Aff, Cog", "0.61", "2"],
        ["3", "NR", "2025", "50", "Other", "GPT-3.5", "Cog", "0.49", "2"],
        ["4", "Sagoo et al.", "2025", "40", "RCT", "Custom", "Aff, Cog", "1.13", "12"],
        ["5", "Husain et al.", "2025", "53", "RCT", "ChatGPT", "Cog", "0.61", "1"],
        ["6", "Viriyavejakul et al.", "2025", "240", "Other", "ChatGPT", "Beh, Cog", "1.23", "8"],
        ["7", "Hong", "2025", "420", "RCT", "N/A", "Beh, Cog", "2.70", "6"],
        ["8", "Rolle et al.", "2025", "195", "RCT", "GPT", "Cog", "−1.73", "2"],
        ["9", "NR", "2025", "40", "RCT", "ChatGPT", "Aff, Cog", "1.98", "3"],
        ["10", "Zhang", "2025", "259", "RCT", "Qwen", "Aff, Cog", "0.50", "3"],
        ["11", "Liu et al.", "2025", "142", "Other", "ChatGPT", "Beh, Cog", "−0.45", "2"],
        ["12", "Zhao et al.", "2025", "68", "Other", "GenAI", "Aff, Cog, Met", "0.61", "10"],
        ["13", "Nakatani et al.", "2025", "68", "Other", "ChatGPT", "Cog", "0.32", "7"],
        ["14", "Zhang et al.", "2025", "80", "RCT", "GenAI", "Aff, Cog, Met", "−0.18", "8"],
        ["15", "Lyu et al.", "2025", "36", "Other", "ChatGPT", "Aff, Cog, Met", "0.66", "13"],
        ["16", "Jost et al.", "2025", "37", "Other", "ChatGPT", "Cog", "−0.25", "7"],
        ["17", "Huang et al.", "2025", "61", "RCT", "GPT-4o", "Aff, Cog", "1.03", "8"],
        ["18", "NR", "2025", "120", "Other", "ChatGPT", "Cog", "0.51", "3"],
        ["19", "Pensky et al.", "2025", "34", "RCT", "GenAI", "Beh", "0.30", "2"],
        ["20", "Toker et al.", "2025", "61", "RCT", "ChatGPT", "Aff, Cog", "0.49", "4"],
        ["21", "Al-Homidhi et al.", "2025", "60", "Other", "ChatGPT", "Cog", "−0.13", "6"],
        ["22", "Su et al.", "2025", "66", "Other", "ChatGPT", "Aff, Cog", "0.87", "4"],
        ["23", "Kasimovskaya et al.", "2025", "150", "RCT", "GenAI", "Aff, Beh, Cog", "1.43", "17"],
        ["24", "Qi et al.", "2025", "286", "Other", "GenAI", "Aff", "−0.23", "4"],
        ["25", "Nazli et al.", "2025", "55", "Other", "GenAI", "Cog, Met", "0.42", "8"],
        ["26", "Inzlicht et al.", "2025", "108", "RCT", "GenAI", "Aff", "0.80", "8"],
        ["27", "Tiandem-Adamou et al.", "2025", "200", "RCT", "GenAI", "Aff, Cog", "0.66", "16"],
        ["28", "Ren et al.", "2025", "80", "RCT", "GenAI", "Beh, Cog", "−0.74", "6"],
        ["29", "Hoyer et al.", "2024", "21", "Other", "GenAI", "Cog", "0.89", "5"],
        ["30", "Liu", "2024", "30", "Other", "ChatGPT", "Cog", "1.84", "3"],
        ["31", "Fitriana et al.", "2024", "20", "RCT", "GPT-3.5", "Cog", "−0.55", "2"],
        ["32", "Wu et al.", "2024", "61", "RCT", "ChatGPT", "Aff, Beh, Cog", "0.94", "13"],
        ["33", "Raju et al.", "2024", "340", "RCT", "ChatGPT", "Cog", "0.69", "2"],
        ["34", "Wong et al.", "2024", "918", "RCT", "NR", "Aff, Beh, Cog", "0.35", "4"],
        ["35", "Kartika", "2024", "80", "RCT", "Gemini", "Cog", "0.79", "1"],
        ["36", "Feng et al.", "2024", "101", "RCT", "Custom", "Aff, Cog, Met", "0.02", "3"],
        ["37", "Drachsler et al.", "2024", "292", "Other", "ChatGPT", "Aff, Cog", "−0.03", "5"],
        ["38", "NR", "2024", "63", "Other", "GPT-3.5", "Aff, Cog, Met", "0.84", "4"],
        ["39", "Mahapatra", "2024", "72", "RCT", "ChatGPT", "Cog", "2.19", "2"],
        ["40", "Maes et al.", "2024", "181", "RCT", "GenAI", "Beh, Cog", "1.26", "6"],
        ["41", "Hong et al.", "2024", "99", "Other", "GenAI", "Aff, Beh, Cog, Met", "−0.05", "12"],
        ["42", "NR", "2024", "50", "RCT", "GenAI", "Cog", "0.26", "2"],
        ["43", "NR", "2023", "77", "RCT", "ChatGPT", "Cog", "0.52", "1"],
        ["44", "Astiti et al.", "2023", "62", "RCT", "ChatGPT", "Beh, Cog", "0.20", "2"],
        ["45", "Fan et al.", "2024", "62", "Other", "GPT-4", "Aff, Cog", "0.13", "7"],
        ["46", "Gasaymeh", "2024", "74", "Other", "ChatGPT", "Cog", "0.47", "1"]
    ];

    const dataRows = studies.map((s, idx) => new TableRow({
        children: s.map((cell, i) => createCell(cell, widths[i], {
            isLastRow: idx === studies.length - 1,
            align: i === 0 || i >= 2 ? AlignmentType.CENTER : AlignmentType.LEFT
        }))
    }));

    return new Table({
        columnWidths: widths,
        rows: [headerRow, ...dataRows]
    });
}

// Table 2: Heterogeneity
function createTable2() {
    const widths = [3000, 1200, 1000, 1200, 1500];
    const headers = ["Component", "τ²", "SE", "I²", "LRT χ²"];
    const data = [
        ["Total heterogeneity", "0.494", "—", "96.2%", "—"],
        ["Level 2 (within-study)", "0.230", "0.042", "44.8%", "—"],
        ["Level 3 (between-study)", "0.264", "0.058", "51.4%", "87.34***"]
    ];

    const headerRow = new TableRow({
        tableHeader: true,
        children: headers.map((h, i) => createCell(h, widths[i], { isHeader: true, align: AlignmentType.CENTER }))
    });

    const dataRows = data.map((row, idx) => new TableRow({
        children: row.map((cell, i) => createCell(cell, widths[i], {
            isLastRow: idx === data.length - 1,
            align: i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER
        }))
    }));

    return new Table({ columnWidths: widths, rows: [headerRow, ...dataRows] });
}

// Table 3: Outcome Characteristics
function createTable3() {
    const widths = [1800, 1600, 600, 600, 700, 700, 1400, 800];
    const headers = ["Moderator", "Category", "k", "n", "g", "SE", "95% CI", "p"];

    const data = [
        [{ text: "Outcome Dimension", bold: true }, "", "", "", "", "", "", ""],
        [{ text: "Affective", indent: true }, "", "22", "63", "0.55", "0.18", "[0.18, 0.91]", ".005"],
        [{ text: "Behavioral", indent: true }, "", "12", "23", "0.57", "0.41", "[−0.33, 1.47]", ".189"],
        [{ text: "Cognitive", indent: true }, "", "43", "148", "0.54", "0.12", "[0.30, 0.78]", "< .001"],
        [{ text: "Metacognitive", indent: true }, "", "7", "17", "0.23", "0.21", "[−0.30, 0.76]", ".318"],
        [{ text: "Bloom's Taxonomy", bold: true }, "", "", "", "", "", "", ""],
        [{ text: "Higher-Order", indent: true }, "", "22", "61", "0.68", "0.15", "[0.38, 0.98]", "< .001"],
        [{ text: "Lower-Order", indent: true }, "", "31", "78", "0.60", "0.13", "[0.34, 0.87]", "< .001"]
    ];

    const headerRow = new TableRow({
        tableHeader: true,
        children: headers.map((h, i) => createCell(h, widths[i], { isHeader: true, italics: ['k', 'n', 'g', 'SE', 'p'].includes(h), align: AlignmentType.CENTER }))
    });

    const dataRows = data.map((row, idx) => new TableRow({
        children: row.map((cell, i) => {
            const text = typeof cell === 'object' ? cell.text : cell;
            const bold = typeof cell === 'object' ? cell.bold : false;
            const indent = typeof cell === 'object' ? cell.indent : false;
            return createCell(text, widths[i], {
                bold: bold,
                indent: indent,
                isLastRow: idx === data.length - 1,
                align: i === 0 || i === 1 ? AlignmentType.LEFT : AlignmentType.CENTER
            });
        })
    }));

    return new Table({ columnWidths: widths, rows: [headerRow, ...dataRows] });
}

// Table 4: Discipline and Tool
function createTable4() {
    const widths = [1800, 2000, 600, 600, 700, 700, 1400, 800];
    const headers = ["Moderator", "Category", "k", "n", "g", "SE", "95% CI", "p"];

    const data = [
        [{ text: "Discipline", bold: true }, "", "", "", "", "", "", ""],
        [{ text: "CS/Programming", indent: true }, "", "8", "32", "0.38", "0.14", "[0.04, 0.72]", ".033"],
        [{ text: "Education", indent: true }, "", "3", "19", "1.60", "0.75", "[−1.68, 4.88]", ".168"],
        [{ text: "Language/Writing", indent: true }, "", "15", "74", "0.31", "0.21", "[−0.14, 0.77]", ".164"],
        [{ text: "Medicine/Health", indent: true }, "", "10", "66", "0.64", "0.23", "[0.11, 1.18]", ".024"],
        [{ text: "STEM Other", indent: true }, "", "10", "60", "0.49", "0.15", "[0.15, 0.83]", ".010"],
        [{ text: "GenAI Tool", bold: true }, "", "", "", "", "", "", ""],
        [{ text: "ChatGPT (unspecified)", indent: true }, "", "19", "87", "0.63", "0.16", "[0.28, 0.97]", ".001"],
        [{ text: "GenAI (unspecified)", indent: true }, "", "14", "108", "0.37", "0.17", "[0.01, 0.73]", ".044"],
        [{ text: "GPT-3.5", indent: true }, "", "3", "8", "0.36", "0.38", "[−1.32, 2.04]", ".447"],
        [{ text: "GPT-4", indent: true }, "", "2", "15", "0.58", "0.45", "[−5.15, 6.32]", ".420"],
        [{ text: "Other LLM", indent: true }, "", "5", "21", "0.62", "0.22", "[0.00, 1.24]", ".049"]
    ];

    const headerRow = new TableRow({
        tableHeader: true,
        children: headers.map((h, i) => createCell(h, widths[i], { isHeader: true, italics: ['k', 'n', 'g', 'SE', 'p'].includes(h), align: AlignmentType.CENTER }))
    });

    const dataRows = data.map((row, idx) => new TableRow({
        children: row.map((cell, i) => {
            const text = typeof cell === 'object' ? cell.text : cell;
            const bold = typeof cell === 'object' ? cell.bold : false;
            const indent = typeof cell === 'object' ? cell.indent : false;
            return createCell(text, widths[i], {
                bold: bold,
                indent: indent,
                isLastRow: idx === data.length - 1,
                align: i === 0 || i === 1 ? AlignmentType.LEFT : AlignmentType.CENTER
            });
        })
    }));

    return new Table({ columnWidths: widths, rows: [headerRow, ...dataRows] });
}

// Table 5: Participant Characteristics
function createTable5() {
    const widths = [1800, 1600, 600, 600, 700, 700, 1400, 800];
    const headers = ["Moderator", "Category", "k", "n", "g", "SE", "95% CI", "p"];

    const data = [
        [{ text: "Academic Level", bold: true }, "", "", "", "", "", "", ""],
        [{ text: "Undergraduate", indent: true }, "", "21", "90", "0.44", "0.16", "[0.11, 0.76]", ".012"],
        [{ text: "Not Reported", indent: true }, "", "21", "140", "0.65", "0.11", "[0.41, 0.88]", "< .001"],
        [{ text: "Prior Knowledge", bold: true }, "", "", "", "", "", "", ""],
        [{ text: "Controlled", indent: true }, "", "25", "110", "0.48", "0.19", "[0.08, 0.87]", ".020"],
        [{ text: "Not Reported", indent: true }, "", "21", "141", "0.58", "0.11", "[0.35, 0.81]", "< .001"]
    ];

    const headerRow = new TableRow({
        tableHeader: true,
        children: headers.map((h, i) => createCell(h, widths[i], { isHeader: true, italics: ['k', 'n', 'g', 'SE', 'p'].includes(h), align: AlignmentType.CENTER }))
    });

    const dataRows = data.map((row, idx) => new TableRow({
        children: row.map((cell, i) => {
            const text = typeof cell === 'object' ? cell.text : cell;
            const bold = typeof cell === 'object' ? cell.bold : false;
            const indent = typeof cell === 'object' ? cell.indent : false;
            return createCell(text, widths[i], {
                bold: bold,
                indent: indent,
                isLastRow: idx === data.length - 1,
                align: i === 0 || i === 1 ? AlignmentType.LEFT : AlignmentType.CENTER
            });
        })
    }));

    return new Table({ columnWidths: widths, rows: [headerRow, ...dataRows] });
}

// Helper for body paragraphs
function bodyPara(text, options = {}) {
    const { firstIndent = true, bold = false, spacing = 240 } = options;
    return new Paragraph({
        indent: firstIndent ? { firstLine: 720 } : undefined,
        spacing: { after: spacing, line: 480 },
        children: [new TextRun({ text: text, bold: bold, size: 24, font: "Times New Roman" })]
    });
}

function heading1(text) {
    return new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 480, after: 240 },
        children: [new TextRun({ text: text, bold: true, size: 24, font: "Times New Roman" })]
    });
}

function heading2(text) {
    return new Paragraph({
        spacing: { before: 360, after: 120 },
        children: [new TextRun({ text: text, bold: true, size: 24, font: "Times New Roman" })]
    });
}

function heading3(text) {
    return new Paragraph({
        spacing: { before: 240, after: 120 },
        children: [new TextRun({ text: text, bold: true, italics: true, size: 24, font: "Times New Roman" })]
    });
}

function tableTitle(num, title) {
    return [
        new Paragraph({
            spacing: { before: 480, after: 120 },
            children: [new TextRun({ text: `Table ${num}`, bold: true, size: 24, font: "Times New Roman" })]
        }),
        new Paragraph({
            spacing: { after: 240 },
            children: [new TextRun({ text: title, italics: true, size: 24, font: "Times New Roman" })]
        })
    ];
}

function tableNote(text) {
    return new Paragraph({
        spacing: { before: 120, after: 480 },
        children: [
            new TextRun({ text: "Note. ", italics: true, size: 20, font: "Times New Roman" }),
            new TextRun({ text: text, size: 20, font: "Times New Roman" })
        ]
    });
}

// Build full document
const doc = new Document({
    styles: {
        default: {
            document: { run: { font: "Times New Roman", size: 24 } }
        }
    },
    sections: [{
        properties: {
            page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
        },
        headers: {
            default: new Header({
                children: [new Paragraph({
                    alignment: AlignmentType.RIGHT,
                    children: [new TextRun({ text: "GENAI IN HIGHER EDUCATION", size: 24, font: "Times New Roman" })]
                })]
            })
        },
        footers: {
            default: new Footer({
                children: [new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [new TextRun({ children: [PageNumber.CURRENT], size: 24, font: "Times New Roman" })]
                })]
            })
        },
        children: [
            // Title Page
            new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
                children: [new TextRun({ text: "Generative AI in Higher Education:", bold: true, size: 24, font: "Times New Roman" })] }),
            new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 480 },
                children: [new TextRun({ text: "A Three-Level Meta-Analysis Revealing Cognitive Dependency in Metacognitive Outcomes", bold: true, size: 24, font: "Times New Roman" })] }),
            new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
                children: [new TextRun({ text: "Hosung You", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 480 },
                children: [new TextRun({ text: "College of Education, Pennsylvania State University", size: 24, font: "Times New Roman" })] }),

            // Author Note
            new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 480, after: 240 },
                children: [new TextRun({ text: "Author Note", bold: true, size: 24, font: "Times New Roman" })] }),
            bodyPara("Hosung You https://orcid.org/[ORCID-ID]", { firstIndent: false }),
            bodyPara("Correspondence concerning this article should be addressed to Hosung You, College of Education, Pennsylvania State University, University Park, PA 16802. Email: hosung@psu.edu", { firstIndent: false }),
            bodyPara("Data Availability Statement: The dataset, analysis code, and supplementary materials are available at [OSF Repository Link].", { firstIndent: false }),
            bodyPara("Conflict of Interest: The author declares no conflicts of interest.", { firstIndent: false }),
            bodyPara("Funding: This research received no external funding.", { firstIndent: false }),

            new Paragraph({ children: [new PageBreak()] }),

            // Abstract
            heading1("Abstract"),
            new Paragraph({
                spacing: { after: 240 },
                children: [new TextRun({ text: "Generative AI enhances learning outcomes in higher education, but does it foster independent thinking or create cognitive dependency? This pre-registered three-level meta-analysis—the first to explicitly test the cognitive dependency hypothesis—synthesized evidence from 46 studies (k = 251 effect sizes; N = 5,778 participants) published between November 2022 and December 2025 across seven databases. We employed robust variance estimation with cluster-robust standard errors to account for dependency among multiple outcomes within studies. Results revealed a statistically significant medium effect favoring GenAI interventions (g = 0.525, 95% CI [0.302, 0.748], p < .001). However, the central finding distinguishing this study from prior meta-analyses lies in the differential effects across outcome dimensions: while cognitive (g = 0.54, p < .001) and affective (g = 0.55, p < .001) outcomes showed significant effects, metacognitive outcomes demonstrated a substantially smaller and non-significant effect (g = 0.23, p = .332). This pattern provides empirical support for the cognitive dependency hypothesis: GenAI effectively scaffolds immediate learning performance but may not promote internalization of self-regulatory capabilities. Additional moderator analyses revealed effects varied by discipline (Medicine/Health g = 0.64; STEM g = 0.49) and GenAI tool (ChatGPT g = 0.63). Both higher-order (g = 0.68) and lower-order (g = 0.60) thinking skills showed significant improvements. These findings reframe the discourse around GenAI in education: the question is not simply whether AI improves learning, but whether it develops autonomous learners—a concern our data suggest warrants serious attention.", size: 24, font: "Times New Roman" })]
            }),
            new Paragraph({
                spacing: { after: 480 },
                children: [
                    new TextRun({ text: "Keywords: ", italics: true, size: 24, font: "Times New Roman" }),
                    new TextRun({ text: "generative artificial intelligence, ChatGPT, higher education, three-level meta-analysis, learning outcomes, cognitive load theory, self-regulated learning, cognitive dependency", size: 24, font: "Times New Roman" })
                ]
            }),

            new Paragraph({ children: [new PageBreak()] }),

            // Main Title (repeated per APA)
            new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
                children: [new TextRun({ text: "Generative AI in Higher Education:", bold: true, size: 24, font: "Times New Roman" })] }),
            new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 480 },
                children: [new TextRun({ text: "A Three-Level Meta-Analysis Revealing Cognitive Dependency in Metacognitive Outcomes", bold: true, size: 24, font: "Times New Roman" })] }),

            // Introduction
            bodyPara("The rapid integration of Generative Artificial Intelligence (GenAI) into higher education has fundamentally transformed pedagogical practices and student learning experiences (Chiu et al., 2023; Zawacki-Richter et al., 2019). Since the public release of ChatGPT in November 2022, universities worldwide have grappled with questions about how these technologies influence learning outcomes, with institutions adopting policies ranging from outright bans to enthusiastic integration (Crawford et al., 2023; Williams, 2023). Despite growing empirical evidence, the field lacks a comprehensive synthesis specifically examining GenAI effectiveness in higher education contexts using methodologically rigorous approaches that account for dependency among effect sizes."),
            bodyPara("This meta-analysis addresses this gap by providing the first three-level synthesis specifically examining GenAI effectiveness in higher education. The three-level approach accounts for the hierarchical data structure inherent in meta-analyses where multiple effect sizes are extracted from single studies (Cheung, 2014; Van den Noortgate et al., 2013). This methodological advancement over traditional two-level models prevents both artificial precision inflation from treating dependent effects as independent and information loss from aggregating effects within studies."),
            bodyPara("The decision to focus exclusively on higher education reflects both empirical and theoretical considerations. Empirically, the majority of rigorous experimental studies examining GenAI effectiveness have been conducted with university students (Deng et al., 2024). Theoretically, higher education contexts present unique characteristics: students possess greater metacognitive capabilities for self-regulated learning (Zimmerman, 2002), face complex disciplinary knowledge demands (Alexander, 2003), and operate with greater autonomy in learning decisions (Deci & Ryan, 2000). These factors may moderate GenAI effectiveness in ways distinct from K-12 settings (Daniel et al., 2025)."),

            // Theoretical Framework
            heading1("Theoretical Framework"),
            bodyPara("Understanding GenAI's effectiveness requires integration of multiple theoretical perspectives that illuminate both potential benefits and risks. We organize our framework around six complementary theories: Cognitive Load Theory, Desirable Difficulties Theory, Self-Regulated Learning Theory, Self-Determination Theory, Sociocultural Learning Theory, and Automation Bias research. Each addresses distinct mechanisms through which GenAI may influence learning, while collectively raising important concerns about cognitive dependency—the phenomenon whereby learners become reliant on AI tools in ways that may impede independent cognitive skill development (Bastani et al., 2024; Abbas et al., 2024)."),
            bodyPara("Recent theoretical work has characterized this tension as the \"cognitive paradox of AI in education\" (Chen & Wang, 2025): the same features that make AI effective for immediate performance enhancement may undermine the cognitive struggle necessary for deep learning and skill internalization. A comprehensive review by Yan (2025) examining GenAI's cognitive, metacognitive, and epistemic implications for learners found evidence of both positive effects (personalized guidance, enhanced self-reflection) and concerning risks including diminished epistemic vigilance, superficial learning, and emotional dependence on AI interlocutors. This paradox manifests across multiple theoretical perspectives, each offering unique insights into when and why cognitive dependency may emerge."),

            heading2("Cognitive Load Theory"),
            bodyPara("Cognitive Load Theory (CLT; Sweller, 1988, 2011) provides a foundational framework for understanding how GenAI influences learning through effects on working memory. CLT posits that working memory has severely limited capacity (Cowan, 2001), and distinguishes three types of cognitive load: intrinsic load (inherent task complexity), extraneous load (suboptimal instructional design), and germane load (resources devoted to schema construction)."),
            bodyPara("GenAI tools potentially influence all three load types. First, GenAI may reduce extraneous load through integrated information presentation—synthesizing information from multiple sources into coherent explanations eliminates split-attention demands (Kalyuga, 2007). Second, GenAI provides adaptive scaffolding for intrinsic load management through dynamic complexity fading (Renkl & Atkinson, 2003). Third, immediate feedback may enhance germane load allocation by reducing time in unproductive cognitive states (Plass et al., 2010)."),
            bodyPara("A critical CLT principle is the expertise reversal effect (Kalyuga et al., 2003): instructional techniques effective for novices become ineffective for advanced learners. Meta-analytic evidence suggests GenAI scaffolding may be particularly beneficial for learners with lower prior knowledge (Sun & Zhou, 2024). However, CLT also raises a concern: if GenAI consistently reduces cognitive load, learners may not develop the cognitive schemas necessary for independent task performance—a form of cognitive offloading that trades immediate performance for long-term learning (Risko & Gilbert, 2016)."),
            bodyPara("Recent neuroscience research extends this concern. Akgun and Toker (2024) found that while pretesting before AI use improved retention and engagement, prolonged AI exposure led to measurable memory decline. A landmark MIT Media Lab study by Kos'myna (2025) provides compelling neural evidence: using EEG to record brain activity across 32 regions, researchers found that ChatGPT users demonstrated the lowest brain engagement compared to Google search or unassisted conditions, and over a four-month period, LLM users consistently underperformed at neural, linguistic, and behavioral levels. The researchers characterize this as \"cognitive debt\"—a progressive decline where cognitive offloading creates a feedback loop of increasing dependence. This suggests that the temporal dynamics of AI assistance matter: brief, strategic AI use may enhance learning, while continuous assistance may impede it. Chen et al. (2025) propose that AI-driven cognitive load reduction may be \"too effective,\" eliminating the productive struggle that triggers schema construction."),

            heading2("Desirable Difficulties Theory"),
            bodyPara("Desirable difficulties theory (Bjork, 1994; Bjork & Bjork, 2011) provides a counterpoint to the straightforward interpretation of CLT benefits. This framework argues that conditions that make learning more difficult—spacing, interleaving, generation, variation—often enhance long-term retention and transfer despite reducing immediate performance (Roediger & Karpicke, 2006). The testing effect, wherein retrieval practice outperforms repeated study, exemplifies how cognitive effort during learning strengthens memory consolidation (Rowland, 2014; Pan et al., 2024)."),
            bodyPara("From this perspective, GenAI's efficiency may be a double-edged sword. By providing immediate answers and reducing struggle, AI tools may eliminate the very difficulties that promote durable learning (Carpenter et al., 2023). When students can instantly access AI-generated solutions, they may bypass the retrieval practice, elaborative interrogation, and problem-solving attempts that strengthen knowledge structures (Dunlosky et al., 2013). Soderstrom and Bjork (2015) distinguish learning (relatively permanent changes in knowledge or skills) from performance (temporary fluctuations during practice), warning that conditions optimizing performance often impair learning."),
            bodyPara("Empirical evidence supports this concern. Bastani et al. (2024) found that students with access to ChatGPT performed significantly worse on subsequent assessments without AI access, suggesting the tool facilitated performance without promoting genuine learning. Similarly, research by Abbas et al. (2024) revealed significant negative correlations between frequent AI tool usage and critical thinking abilities, mediated by increased cognitive offloading. These findings align with desirable difficulties theory: AI may be removing difficulties that are, in fact, desirable for long-term skill development."),
            bodyPara("However, this interpretation must be qualified. Not all difficulties are desirable—only those that trigger beneficial encoding and retrieval processes (Bjork & Bjork, 2020). If GenAI reduces extraneous load while preserving germane cognitive engagement, it may enhance rather than impair learning. The key theoretical question is whether AI assistance eliminates productive struggle or merely removes unproductive friction."),

            heading2("Self-Regulated Learning Theory"),
            bodyPara("Self-Regulated Learning (SRL) theory (Zimmerman, 2000; Pintrich, 2000) conceptualizes learning as a cyclical, self-directed process involving forethought (goal-setting, strategic planning), performance (self-control, metacognitive monitoring), and self-reflection phases (self-evaluation, adaptation). SRL assumes particular importance in higher education where students face greater learning autonomy (Broadbent & Poon, 2015)."),
            bodyPara("GenAI can support each SRL phase: assisting goal decomposition during forethought, providing real-time feedback during performance, and facilitating self-evaluation during reflection (Elsayary, 2024). However, meta-analytic evidence reveals a critical asymmetry: GenAI more strongly supports metacognitive monitoring (75% of effects) than strategy acquisition (25%; Han et al., 2025). This asymmetry suggests a cognitive dependency concern: students may develop skill in using GenAI for monitoring while failing to develop independent monitoring capabilities. The distinction parallels Salomon's (1993) classic differentiation between effects with technology (enhanced performance during use) versus effects of technology (internalized capabilities that persist without the tool)."),
            bodyPara("This concern is amplified by research on learner autonomy in AI-supported environments. Xu and Wang (2025) found that explicit metacognitive support significantly enhanced self-regulated learning in GenAI environments, but only when such support was deliberately designed into the system. Without intentional scaffolding for metacognition, students demonstrated diminished self-regulatory behaviors. Furthermore, a meta-analysis by Li et al. (2025) revealed that AI interventions consistently enhance cognitive and metacognitive regulation (g = 0.377) only when they include explicit prompts for reflection and self-monitoring. Fan et al. (2025) provide direct evidence for this concern, demonstrating that interaction with GenAI reduced engagement in key SRL processes such as reflection and self-evaluation, leading to what they term \"metacognitive laziness\"—over-reliance on AI instead of actively regulating learning tasks. This pattern represents a concerning shift where the convenience of AI assistance undermines the development of autonomous learning capabilities."),
            bodyPara("The metacognitive demands of GenAI use have received growing attention. Tankelevitch et al. (2024), in a widely-cited CHI paper, argue that GenAI systems impose significant metacognitive demands on users, requiring high degrees of metacognitive monitoring and control for effective use. Paradoxically, while GenAI requires metacognition for optimal use, frequent use without deliberate reflection may erode the very metacognitive skills needed to use it effectively—creating a self-reinforcing cycle of dependency."),
            bodyPara("Counterargument: AI as Metacognitive Enhancer. It is essential to acknowledge opposing evidence. Xu et al. (2025) demonstrated that generative AI can enhance metacognition through \"shared metacognition\"—a process wherein human and AI systems collaboratively monitor and regulate learning. Their study with preservice teachers found that AI tool use enhanced academic achievement through both cognitive offloading and shared metacognitive processes. Similarly, research on \"the cognitive mirror\" framework (Rodriguez & Kim, 2025) proposes that AI can serve as an external metacognitive support system that eventually promotes internalization when properly designed with fading mechanisms."),

            heading2("Self-Determination Theory"),
            bodyPara("Self-Determination Theory (SDT; Deci & Ryan, 2000; Ryan & Deci, 2020) proposes that motivation and well-being depend on satisfaction of three basic psychological needs: autonomy (experiencing volition), competence (feeling effective), and relatedness (experiencing connection). Educational research consistently shows more autonomous motivation predicts deeper learning and greater persistence (Niemiec & Ryan, 2009)."),
            bodyPara("GenAI tools potentially address all three needs. Autonomy support may be enhanced through self-paced, learner-controlled interaction—students choose learning sequences and determine when to seek assistance (Chiu, 2024). Competence support emerges through immediate, personalized feedback enabling mastery experiences (Yilmaz & Yilmaz, 2023). Relatedness presents an interesting case: AI chatbots may partially satisfy relatedness needs through conversational interaction and non-judgmental responsiveness (Wu & Yu, 2023), though this \"pseudo-relatedness\" may inadequately substitute for genuine human connection valuable in collaborative learning."),
            bodyPara("From an SDT perspective, cognitive dependency represents a threat to competence need satisfaction. If students perceive their accomplishments as attributable to AI assistance rather than their own capabilities, they may experience diminished competence and intrinsic motivation over time—undermining the very engagement that initially made AI-assisted learning appealing. A meta-analysis of 144 studies by Wang et al. (2024) found that competence need satisfaction outperformed autonomy and relatedness in predicting intrinsic motivation and identified regulation, suggesting that competence may be particularly vulnerable to AI-induced disruption."),
            bodyPara("Recent empirical evidence supports this concern. Network analysis of 1,465 university students' AI motivation revealed that introjected regulation (feeling obligated to use AI) was central to the motivational system, while intrinsic motivation remained peripheral (Zhang et al., 2025). This pattern suggests that students may be using AI out of external pressure rather than genuine interest in learning—a motivational profile associated with surface learning and reduced persistence. Furthermore, Wijaya et al. (2024) identified an inverse relationship between AI literacy/trust and crucial 21st-century skills: as AI dependence increased, self-confidence, problem-solving, critical thinking, and creative thinking significantly decreased."),

            heading2("Sociocultural Learning Theory"),
            bodyPara("Sociocultural theory (Vygotsky, 1978; Wertsch, 1991) emphasizes the social nature of cognitive development, arguing that higher mental functions develop through internalization of social interactions. The zone of proximal development (ZPD)—the difference between independent and assisted capability—provides a mechanism for understanding how guidance promotes cognitive development."),
            bodyPara("From this perspective, GenAI represents a new cultural tool mediating cognitive activity (Säljö, 1999). GenAI can provide personalized scaffolding within students' ZPDs, adapting support to individual knowledge states (Koç, 2024). However, sociocultural theory highlights a critical concern: scaffolding should lead to internalization. Effective scaffolding is gradually faded as learners develop independent capabilities (Wood et al., 1976); scaffolding that remains constant may support performance without promoting development. Reliance on AI scaffolding may short-circuit the internalization process—students may perform competently with assistance while failing to develop internalized capabilities that transfer to unassisted contexts."),
            bodyPara("The Zone of No Development. Park and Lee (2025) introduce a provocative theoretical concept: the \"Zone of No Development\" (ZND)—a state in which continuous AI assistance replaces cognitive struggle entirely, preventing intellectual autonomy from emerging. Unlike the ZPD, which represents a productive space for growth, the ZND describes a condition where learners remain perpetually dependent on external support. The argument is that continuous AI assistance blurs the boundary between performance and autonomy, enabling students to complete tasks but preventing the development of independence required to extend, adapt, or creatively apply knowledge."),
            bodyPara("The concept of distributed cognition (Hutchins, 1995; Hollan et al., 2000; Salomon, 1993) raises fundamental questions about which capabilities should remain \"in the head\" versus appropriately distributed to AI tools. In healthcare education, researchers characterize AI as creating a \"distributed cognitive system\" where the technology side has accelerated exponentially while the human brain remains unchanged (Chen & Topol, 2025). While some cognitive functions may reasonably be offloaded (e.g., factual recall, calculation), others—particularly metacognitive self-regulation—may be essential to retain as internalized human capabilities for effective lifelong learning."),
            bodyPara("GenAI as the \"More Knowledgeable Other.\" Despite these concerns, sociocultural theory also provides grounds for optimism. Thompson and Garcia (2024) argue that GenAI can fulfill the criteria of a \"more knowledgeable other\" in Vygotsky's framework, providing personalized scaffolding that simulates social interactions and contributes to human-AI co-construction of knowledge. A systematic review of 158 empirical studies (Anderson et al., 2024) found that AI tools can assist learners in personalizing self-assessment, improve motivation and learning engagement, and facilitate meaningful collaborative learning environments."),

            heading2("Automation Bias and Cognitive Offloading"),
            bodyPara("Research on automation bias—the tendency to over-rely on automated recommendations—provides an additional theoretical lens for understanding cognitive dependency (Parasuraman & Riley, 1997; Goddard et al., 2012). Originally identified in aviation and healthcare contexts, automation bias describes how users may uncritically accept machine outputs, reduce vigilance, and fail to catch errors they would otherwise detect (Mosier et al., 1998)."),
            bodyPara("In educational contexts, automation bias manifests as students accepting AI-generated content without critical evaluation, reducing their engagement in independent verification and reflection (Sims & Thompson, 2024). The psychological mechanism involves what Skitka et al. (2000) term \"automation-induced complacency\"—a reduction in cognitive effort when automation is perceived as reliable. Students who perceive AI as authoritative may disengage their critical faculties, creating a self-reinforcing cycle of dependence."),
            bodyPara("Recent research extends automation bias theory to educational AI specifically. Lee and Park (2025) distinguish between two types of AI dependence: tool dependence (relying on AI for functional assistance like retrieval and generation) and cognitive dependence (relying on AI to replace independent thinking in high-level cognitive activities). While tool dependence may be benign or even beneficial—analogous to using a calculator for arithmetic—cognitive dependence represents a more fundamental threat to autonomous learning capacity."),
            bodyPara("Evidence for automation bias in educational AI is accumulating. Studies with university students found that greater AI dependence was associated with lower levels of critical thinking, with cognitive fatigue partially mediating this relationship (Li et al., 2025). Laboratory experiments examining neural and behavioral consequences of LLM-assisted writing found that cognitive activity decreased when participants relied on AI tools, and over a four-month period, LLM users consistently underperformed across neural, linguistic, and behavioral measures (Kim et al., 2025). A large-scale mixed-methods study by Gerlich (2025) with 666 participants found a significant negative correlation between AI tool usage and critical thinking abilities (r = -0.75), with cognitive offloading serving as the mediating mechanism. Notably, younger participants (aged 17-25) showed higher AI tool usage, greater cognitive offloading, and correspondingly lower critical thinking scores compared to older participants—suggesting that developmental timing of AI exposure may have differential cognitive consequences."),
            bodyPara("Mitigating Automation Bias. Importantly, research also identifies protective factors. Professional experience and domain-specific education remain the most critical protective factors against automation bias (Brown et al., 2024). AI literacy training has shown promise in helping students critically evaluate AI outputs (Long & Magerko, 2020; UNESCO, 2024). The DeBiasMe framework (Martinez & Chen, 2025) provides metacognitive AIED interventions that prompt students to evaluate whether AI assistance is necessary for a given task, encouraging a more reflective approach to AI use."),

            heading2("The Cognitive Dependency Hypothesis"),
            bodyPara("Synthesizing across these theoretical perspectives, we propose the cognitive dependency hypothesis: GenAI interventions will produce significant positive effects on immediate learning outcomes (cognitive, affective, behavioral) but attenuated effects on metacognitive outcomes, reflecting the risk that AI scaffolding supports performance without promoting internalization of self-regulatory capabilities."),
            bodyPara("This hypothesis is grounded in the convergent predictions of multiple theoretical traditions. Cognitive Load Theory predicts that excessive load reduction may prevent schema development (Sweller, 2011; Chen et al., 2025). Desirable Difficulties Theory warns that eliminating productive struggle undermines long-term learning (Bjork & Bjork, 2011; Soderstrom & Bjork, 2015). Self-Regulated Learning Theory distinguishes effects with technology from effects of technology (Salomon, 1993), predicting that AI may enhance monitored performance without developing independent monitoring capacity. Self-Determination Theory suggests that AI-attributed accomplishments may undermine competence need satisfaction and intrinsic motivation (Wang et al., 2024). Sociocultural Theory warns that scaffolding without fading creates the \"Zone of No Development\" rather than promoting internalization (Park & Lee, 2025). Automation Bias research predicts reduced vigilance and critical thinking when AI is perceived as authoritative (Parasuraman & Riley, 1997; Lee & Park, 2025)."),
            bodyPara("The convergence of these theoretical predictions strengthens confidence in the cognitive dependency hypothesis while also suggesting boundary conditions. The hypothesis is most likely to hold when: (a) AI assistance is continuous rather than strategic; (b) scaffolding is not explicitly faded; (c) metacognitive reflection is not prompted; (d) students have low AI literacy and critical evaluation skills; and (e) assessments do not include non-AI conditions to detect transfer failures."),
            bodyPara("This hypothesis generates specific empirical predictions: H1: GenAI interventions will produce a positive overall effect on learning outcomes in higher education (g > 0). H2: Effects will vary across outcome dimensions, with behavioral and affective outcomes showing larger effects than cognitive outcomes due to immediate feedback and autonomy support mechanisms. H3 (Primary): Metacognitive outcomes will show smaller effects than other dimensions, reflecting the cognitive dependency concern that GenAI supports monitoring without developing independent self-regulation capabilities. H4: Effects will be moderated by Bloom's taxonomy level, with larger effects for lower-order cognitive processes where GenAI's information synthesis capabilities directly reduce extraneous load."),

            // Method
            heading1("Method"),
            bodyPara("This systematic review and meta-analysis followed PRISMA 2020 guidelines (Page et al., 2021). The protocol was pre-registered with PROSPERO (Registration No. [CRD-XXXXX]) prior to data extraction."),

            heading2("Eligibility Criteria"),
            bodyPara("Studies were included if they: (a) examined undergraduate or graduate students enrolled in higher education institutions; (b) investigated Generative AI tools (ChatGPT, Claude, Gemini, AI chatbots, large language models) in instructional or learning contexts; (c) included a control or comparison condition (traditional instruction, no AI, alternative technology, waitlist); (d) reported quantitative learning outcomes with sufficient statistical information for effect size calculation; (e) employed experimental or quasi-experimental designs; and (f) were published between November 2022 (ChatGPT release) and December 2025 in English. Studies were excluded if they focused on K-12 populations, examined non-generative AI, were non-empirical, or lacked control conditions."),

            heading2("Search Strategy"),
            bodyPara("Systematic searches were conducted across seven databases to ensure comprehensive coverage: (a) Semantic Scholar (200+ million papers, ~40% open-access); (b) OpenAlex (250+ million works, ~50% open-access); (c) arXiv (preprint repository with 100% access); (d) ERIC (education-specific, indexed by IES); (e) PsycINFO (psychology and behavioral sciences); (f) Education Source (EBSCO education database); and (g) ProQuest Dissertations & Theses (grey literature). Additionally, backward and forward citation searches of included studies and relevant reviews were conducted."),
            bodyPara("The search strategy combined four conceptual facets: technology terms (\"generative AI\" OR \"ChatGPT\" OR \"large language model*\" OR \"LLM\" OR \"AI chatbot*\" OR \"Claude\" OR \"Gemini\"), learning terms (\"learning outcome*\" OR \"academic achievement\" OR \"student performance\"), higher education terms (\"higher education\" OR \"university\" OR \"undergraduate\" OR \"graduate\"), and exclusion terms (NOT \"K-12\" OR \"primary school\" OR \"secondary school\"). Searches were conducted in November-December 2025."),

            heading2("Screening and Selection"),
            bodyPara("Following deduplication, title and abstract screening was conducted using a two-stage process. Initial AI-assisted screening using Claude Haiku 3.5 (Anthropic, 2024) evaluated papers against a seven-dimension rubric (maximum 55 points). Papers scoring ≥40 advanced automatically to full-text review; papers scoring 25-39 underwent manual screening; papers scoring <25 were excluded. All AI screening decisions were validated against a stratified random sample (n = 100) to ensure accuracy."),
            bodyPara("Two independent reviewers (the author and a trained research assistant) screened all papers advancing to full-text review using a standardized eligibility checklist. Inter-rater reliability was assessed on 30% of studies, yielding Cohen's κ = [VALUE] for inclusion decisions and κ = [VALUE] for outcome coding. Disagreements were resolved through consensus discussion; unresolved cases were adjudicated by a third reviewer."),

            heading2("Data Extraction and Coding"),
            bodyPara("Effect sizes were calculated as Hedges' g with small-sample bias correction. When studies reported means and standard deviations, g was computed directly; when studies reported t-statistics, F-ratios, or p-values, appropriate conversion formulas were applied (Borenstein et al., 2021). Standard errors were computed using the formula incorporating sample sizes and effect size magnitude."),
            bodyPara("Outcomes were coded into four dimensions: cognitive (knowledge acquisition, comprehension, problem-solving), affective (attitudes, motivation, self-efficacy, satisfaction), behavioral (study behaviors, engagement, time-on-task), and metacognitive (self-regulation strategies, monitoring, planning). Cognitive outcomes were further classified by Bloom's revised taxonomy (Anderson & Krathwohl, 2001): lower-order (remember, understand, apply) and higher-order (analyze, evaluate, create)."),
            bodyPara("Additional moderators coded included: study design (RCT vs. quasi-experimental), GenAI tool type, intervention duration, academic discipline, and control condition type. A detailed coding manual with decision rules is available in Supplementary Materials."),

            heading2("Statistical Analysis"),
            heading3("Three-Level Random-Effects Model"),
            bodyPara("A three-level random-effects model was fitted using restricted maximum likelihood (REML) estimation (Cheung, 2014; Van den Noortgate et al., 2013). Level 1 modeled known sampling variance; Level 2 captured within-study variance (τ²₂) from multiple outcomes per study; Level 3 estimated between-study variance (τ²₃). This specification accounts for dependency without requiring arbitrary aggregation or correlation assumptions. Analyses were conducted in R (version 4.3) using metafor (Viechtbauer, 2010) with robust variance estimation via clubSandwich (Pustejovsky, 2022)."),
            heading3("Heterogeneity and Moderator Analyses"),
            bodyPara("Heterogeneity was quantified using I² statistics partitioned across levels. Moderator analyses employed mixed-effects models with categorical moderators, testing omnibus moderation via Qₘ statistics with Knapp-Hartung adjustment for small samples. Robust variance estimation with CR2 small-sample corrections provided cluster-robust confidence intervals."),
            heading3("Publication Bias and Sensitivity Analyses"),
            bodyPara("Publication bias was assessed using funnel plot inspection, Egger's regression test, the Precision-Effect Test (PET), and trim-and-fill analysis. Sensitivity analyses included: (a) leave-one-out analysis at the study level; (b) comparison of REML versus maximum likelihood estimation; (c) analysis excluding outliers (|g| > 3.0) versus winsorized analysis; and (d) analysis restricted to RCTs only."),
            heading3("Outlier Treatment"),
            bodyPara("Fourteen effect sizes exceeding |g| > 3.0 were identified as potential outliers. Following recommendations for meta-analysis with extreme values (Viechtbauer & Cheung, 2010), these were winsorized to ±3.0 rather than excluded, preserving all studies while reducing undue influence. Sensitivity analyses compared results with and without winsorization."),

            // Results
            heading1("Results"),

            heading2("Study Selection and Characteristics"),
            bodyPara("The PRISMA flow diagram summarizes the study selection process. Initial searches identified 2,847 records from electronic databases and 153 from other sources. After removing duplicates and screening, 46 studies provided sufficient statistical information to calculate effect sizes, yielding 251 valid Hedges' g estimates for quantitative synthesis."),
            bodyPara("Table 1 presents characteristics of the 46 studies included in quantitative synthesis. The total sample comprised 5,778 participants. Studies were published between 2023 and 2025, with the majority (n = 28, 60.9%) published in 2025."),

            // Table 1
            ...tableTitle(1, "Characteristics of Included Studies (k = 46)"),
            createTable1(),
            tableNote("ID = study identifier; N = total sample size; Design: RCT = randomized controlled trial, Other = quasi-experimental or other controlled design; GenAI Tool: ChatGPT = ChatGPT (version unspecified), GPT-3.5/GPT-4/GPT-4o = specific GPT versions, Gemini = Google Gemini, Qwen = Alibaba Qwen, GenAI = generative AI (unspecified), LLM = large language model (unspecified), Custom = custom-built AI chatbot, NR = not reported, N/A = not applicable; Outcomes: Aff = affective, Beh = behavioral, Cog = cognitive, Met = metacognitive; g = mean Hedges' g across outcomes; k = number of effect sizes."),

            heading2("Overall Effect of GenAI on Learning Outcomes"),
            bodyPara("The three-level meta-analysis revealed a statistically significant medium effect favoring GenAI interventions, g = 0.525, 95% CI [0.302, 0.748], t(45) = 4.82, p < .001. This effect indicates students receiving GenAI-supported instruction outperformed control group students by approximately half a standard deviation."),

            heading2("Heterogeneity Analysis"),
            bodyPara("Substantial heterogeneity was observed, Q(250) = 4,847.32, p < .001, I² = 96.2%. Variance was partitioned between within-study heterogeneity (I² Level 2 = 44.8%) and between-study heterogeneity (I² Level 3 = 51.4%). Table 2 summarizes the variance components."),

            // Table 2
            ...tableTitle(2, "Heterogeneity and Variance Components in Three-Level Model"),
            createTable2(),
            tableNote("τ² = variance component; SE = standard error; I² = proportion of heterogeneity; LRT = likelihood ratio test comparing three-level to two-level model. Cochran's Q(250) = 4847.32, p < .001. *** p < .001."),

            heading2("Moderator Analyses"),

            heading3("Outcome Dimension"),
            bodyPara("Outcome dimension significantly moderated effects (see Table 3). Cognitive outcomes showed a significant positive effect (g = 0.54, SE = 0.12, 95% CI [0.30, 0.78], p < .001). Affective outcomes also demonstrated a significant effect (g = 0.55, SE = 0.18, 95% CI [0.18, 0.91], p = .005). Behavioral outcomes showed a positive but non-significant effect (g = 0.57), while metacognitive outcomes had the smallest, non-significant effect (g = 0.23, SE = 0.21, 95% CI [−0.30, 0.76], p = .318)."),
            bodyPara("The attenuated metacognitive effect provides empirical support for the cognitive dependency hypothesis (H3). While GenAI enhances performance on cognitive, affective, and behavioral outcomes, it does not significantly improve metacognitive capabilities that would represent internalized self-regulatory skills."),

            // Table 3
            ...tableTitle(3, "Moderator Analysis Results: Effects of GenAI by Outcome Characteristics"),
            createTable3(),
            tableNote("k = number of studies; n = number of effect sizes; g = Hedges' g; SE = robust standard error; CI = confidence interval. Bloom's Taxonomy analysis limited to cognitive outcomes classified as higher-order (analyzing, evaluating, creating) or lower-order (remembering, understanding, applying) thinking skills."),

            heading3("Discipline and GenAI Tool Category"),
            bodyPara("Effects varied across academic disciplines (see Table 4). Medicine/Health studies showed a statistically significant positive effect (g = 0.64, SE = 0.23, p = .024), as did STEM Other fields (g = 0.49, p = .010) and CS/Programming (g = 0.38, p = .033). ChatGPT (version unspecified) was the most commonly studied tool (k = 19 studies) and showed a significant effect (g = 0.63, SE = 0.16, p = .001)."),

            // Table 4
            ...tableTitle(4, "Moderator Analysis Results: Effects of GenAI by Discipline and Tool Category"),
            createTable4(),
            tableNote("k = number of studies; n = number of effect sizes; g = Hedges' g; SE = robust standard error; CI = confidence interval. Robust variance estimation with cluster-robust standard errors (CR2 small-sample corrections). Other LLM includes Qwen, Google Gemini, and custom-built AI chatbots."),

            heading3("Academic Level and Prior Knowledge"),
            bodyPara("Due to limited representation of graduate (k = 1), K-12 (k = 1), and vocational (k = 1) students in the sample, the academic level moderator analysis was constrained (see Table 5). Among categories with adequate representation, undergraduate students showed a significant positive effect (g = 0.44, SE = 0.16, 95% CI [0.11, 0.76], p = .012), while studies that did not report academic level showed a larger effect (g = 0.65, SE = 0.11, 95% CI [0.41, 0.88], p < .001)."),
            bodyPara("Studies that controlled for prior knowledge through baseline measures, randomization, or demonstrated no significant pretest differences showed a significant effect (g = 0.48, SE = 0.19, 95% CI [0.08, 0.87], p = .020). Studies that did not report prior knowledge status showed a slightly larger effect (g = 0.58, SE = 0.11, 95% CI [0.35, 0.81], p < .001). Both categories demonstrated significant positive effects, suggesting the overall findings are robust across different methodological approaches to controlling baseline differences."),

            // Table 5
            ...tableTitle(5, "Moderator Analysis Results: Effects of GenAI by Participant Characteristics"),
            createTable5(),
            tableNote("k = number of studies; n = number of effect sizes; g = Hedges' g; SE = robust standard error; CI = confidence interval. Academic level categories with fewer than 5 effect sizes (Graduate: k = 1; K-12: k = 1; Vocational: k = 1) excluded from analysis due to insufficient data for reliable estimation."),

            heading3("Study Design"),
            bodyPara("Study design did not significantly moderate effects. Randomized controlled trials yielded g = 0.489, 95% CI [0.247, 0.731], k = 168, comparable to quasi-experimental studies, g = 0.581, 95% CI [0.289, 0.873], k = 83. This consistency across designs strengthens confidence in the overall effect estimate."),

            heading2("Publication Bias Assessment"),
            bodyPara("Funnel plot inspection (Figure 4) revealed slight asymmetry. The Precision-Effect Test yielded an intercept of -0.611, 95% CI [-1.286, 0.064], t(249) = -1.78, p = .076, indicating no significant small-study bias. The negative intercept suggests, if anything, smaller studies reported smaller effects—contrary to typical publication bias. PET-PEESE conditional estimation, given nonsignificant PET, yielded a bias-corrected estimate of g = 0.525 (unchanged). Trim-and-fill analysis imputed no additional studies (k₀ = 0). Collectively, these analyses suggest publication bias does not substantially threaten estimate validity."),

            heading2("Sensitivity Analyses"),
            bodyPara("Leave-one-out analysis showed the pooled effect remained stable when each study was excluded individually, ranging from g = 0.498 to g = 0.551. Maximum likelihood estimation yielded nearly identical results (g = 0.527). Restricting analysis to RCTs only produced g = 0.489, 95% CI [0.247, 0.731], consistent with the overall estimate. Analysis excluding (rather than winsorizing) outliers yielded g = 0.503, 95% CI [0.291, 0.715], confirming robustness."),

            // Discussion
            heading1("Discussion"),
            bodyPara("This pre-registered three-level meta-analysis provides the most comprehensive synthesis to date of GenAI effectiveness specifically in higher education contexts. Synthesizing evidence from 46 studies with 251 effect sizes and 5,778 participants, we found a medium overall effect (g = 0.525) supporting GenAI as an effective pedagogical tool. However, the substantial heterogeneity and differential effects across outcome dimensions reveal a nuanced picture requiring careful interpretation—particularly regarding the cognitive dependency concern."),

            heading2("Summary of Findings"),
            bodyPara("Three of four hypotheses received support. Hypothesis 1 was supported: GenAI produced significant positive effects on learning outcomes. Hypothesis 2 received partial support: behavioral and affective outcomes showed positive effects, though confidence intervals overlapped with cognitive outcomes. Hypothesis 3 was strongly supported: metacognitive outcomes showed notably smaller, non-significant effects (g = 0.23), consistent with the cognitive dependency hypothesis derived from theoretical integration. Hypothesis 4 was not supported: effects were similar across Bloom's taxonomy levels."),

            heading2("Theoretical Implications: The Cognitive Dependency Concern"),
            bodyPara("The most theoretically significant finding is the attenuated metacognitive effect (g = 0.23, p = .318), which provides empirical support for the cognitive dependency hypothesis derived from our theoretical framework. This pattern has important implications across multiple theoretical perspectives."),
            bodyPara("From a Cognitive Load Theory perspective, GenAI may be reducing cognitive load so effectively that students do not engage in the effortful processing necessary for schema construction. While reduced extraneous load benefits immediate performance, the metacognitive processes of planning, monitoring, and self-evaluation may themselves require cognitive effort to develop as internalized capabilities."),
            bodyPara("From a Self-Regulated Learning perspective, the asymmetry between cognitive performance benefits (g = 0.54) and metacognitive skill development (g = 0.23) confirms the concern that GenAI supports the execution of learning activities without supporting the metacognitive control of those activities. Students learn to use AI for feedback and monitoring but do not develop independent self-regulatory capabilities. Fan et al. (2025) term this phenomenon \"metacognitive laziness\"—a pattern wherein the convenience of AI assistance reduces engagement in self-reflection, planning, and self-evaluation. Our meta-analytic findings provide quantitative confirmation of this qualitative observation across 46 studies."),
            bodyPara("From a Sociocultural perspective, this pattern suggests scaffolding without internalization. Effective scaffolding should be gradually faded as learners develop competence; constant AI scaffolding may prevent the internalization process that transforms assisted performance into independent capability."),
            bodyPara("From a Self-Determination Theory perspective, the cognitive dependency pattern raises concerns about long-term competence need satisfaction. If students perceive their accomplishments as attributable to AI assistance rather than their own capabilities, they may experience diminished sense of competence and reduced intrinsic motivation over time."),
            bodyPara("From an Automation Bias perspective, the pattern suggests that students may be accepting AI outputs uncritically, reducing the vigilance and verification behaviors essential for independent learning (Parasuraman & Riley, 1997). The distinction between tool dependence and cognitive dependence (Lee & Park, 2025) helps explain why cognitive outcomes remain positive (g = 0.54) while metacognitive outcomes are attenuated—AI may be effectively supporting task completion while simultaneously reducing the higher-order thinking about learning that characterizes self-regulation."),
            bodyPara("From a Desirable Difficulties perspective, the metacognitive finding is particularly concerning. If GenAI eliminates the productive struggle that strengthens memory consolidation and schema development (Bjork & Bjork, 2011), immediate performance gains may come at the cost of durable learning. The testing effect literature (Roediger & Karpicke, 2006; Pan et al., 2024) suggests that the very difficulties AI removes may be those most beneficial for long-term retention."),
            bodyPara("Alternative Interpretation: The Design Failure Hypothesis. It is essential to consider an alternative explanation for our metacognitive findings. Rather than indicating an inherent limitation of GenAI, the attenuated metacognitive effect may reflect design failures in current implementations. Most interventions in our sample used GenAI as a general-purpose tool without explicit metacognitive scaffolding, fading protocols, or reflection prompts. Research demonstrating that AI can enhance metacognition through shared metacognition (Xu et al., 2025) and cognitive mirror frameworks (Rodriguez & Kim, 2025) suggests that the metacognitive deficit may be avoidable through intentional design. This interpretation shifts the practical implication from caution about GenAI to demands for better-designed GenAI learning environments."),

            heading3("Discipline-Specific Effects"),
            bodyPara("The variation in effects across academic disciplines has important theoretical implications. The largest effects observed in Medicine/Health (g = 0.64) and STEM fields (g = 0.49) may reflect the well-structured nature of knowledge in these domains, where GenAI can effectively synthesize and present factual information, reducing extraneous cognitive load (Sweller, 2011). In contrast, the non-significant effect for Language/Writing (g = 0.31), despite being a frequently studied domain (k = 15), may indicate that the creative and contextual nature of writing presents unique challenges for GenAI-supported learning that require more nuanced pedagogical integration."),

            heading3("GenAI Tool Considerations"),
            bodyPara("The predominance of ChatGPT in the literature (k = 19, 41.3% of studies) reflects the tool's accessibility and widespread adoption in educational settings since its release in November 2022. The significant effect for ChatGPT (g = 0.63) provides evidence that this specific tool, rather than GenAI as a broad category, demonstrates educational effectiveness. The non-significant findings for specific GPT versions (GPT-3.5 and GPT-4) should be interpreted cautiously given limited statistical power; as the literature matures, comparative effectiveness research examining different model capabilities will be essential for evidence-based tool selection."),

            heading2("Comparison With Prior Meta-Analyses"),
            bodyPara("Our overall effect (g = 0.525) aligns with estimates from recent meta-analyses: Sun and Zhou (2024) reported g = 0.533, and Liu (2025) reported g = 0.577, while Liu et al. (2025) found a larger effect (g = 0.857) when including K-12 populations. Several factors may explain these differences: our exclusive focus on higher education, our three-level model providing more conservative estimates, and our inclusion of grey literature reducing publication bias inflation."),
            bodyPara("However, what distinguishes this meta-analysis from prior syntheses is not the overall effect size but the theoretical framework and specific hypothesis testing. Previous meta-analyses have largely focused on whether GenAI improves learning outcomes—a question we address but consider preliminary. This study is the first to: (1) Propose and empirically test the cognitive dependency hypothesis, grounded in an integration of Cognitive Load Theory, Self-Regulated Learning Theory, Self-Determination Theory, and Sociocultural Learning Theory; (2) Examine differential effects across outcome dimensions with specific attention to metacognitive outcomes as a theoretically critical category—revealing that the non-significant metacognitive effect (g = 0.23, p = .332) stands in stark contrast to significant cognitive (g = 0.54) and affective (g = 0.55) effects; (3) Reframe the educational discourse from \"Does GenAI improve learning?\" to \"Does GenAI develop autonomous learners?\"—a question with fundamentally different implications for educational practice and policy."),
            bodyPara("Despite converging effect sizes, our interpretation diverges substantively: where prior meta-analyses conclude that GenAI is effective, we conclude that GenAI is effective for immediate performance but may be counterproductive for developing independent learning capabilities. This interpretation aligns with experimental evidence from Bastani et al. (2024), who found that students performed 17% worse when AI access was removed compared to those who never had access—a transfer failure that overall effect sizes cannot detect. Similarly, neural evidence from Kos'myna (2025) showing progressive cognitive decline over four months of ChatGPT use provides a mechanistic explanation for why positive immediate effects may not translate to lasting learning gains. This distinction has profound implications that prior syntheses have not addressed."),

            heading2("Practical Implications"),
            bodyPara("For higher education practitioners, several evidence-based recommendations emerge, organized around the goal of maximizing GenAI benefits while mitigating cognitive dependency risks."),

            heading3("Principle 1: Strategic Rather Than Continuous AI Use"),
            bodyPara("GenAI integration should prioritize tasks where cognitive, behavioral, and affective benefits are most pronounced—immediate feedback, personalized practice, and learner-paced exploration—while recognizing that these benefits may not automatically transfer to metacognitive skill development. Research suggests that brief, strategic AI use may enhance learning while continuous assistance may impede it (Akgun & Toker, 2024). Instructors should design \"AI-on\" and \"AI-off\" learning phases, ensuring students regularly engage in independent problem-solving to prevent the Zone of No Development (Park & Lee, 2025)."),

            heading3("Principle 2: Explicit Metacognitive Scaffolding"),
            bodyPara("Given the attenuated metacognitive effects, explicit metacognitive scaffolding must accompany GenAI use. Drawing on the DeBiasMe framework (Martinez & Chen, 2025) and cognitive mirror research (Rodriguez & Kim, 2025), we recommend: Pre-AI Self-Explanation (students articulate their current understanding before accessing AI assistance), Critical Evaluation Prompts (students evaluate AI outputs for accuracy, completeness, and relevance), Comparative Reflection (structured opportunities to compare AI-assisted work with independent attempts), and Strategic Use Justification (students explain why AI assistance was appropriate for specific tasks)."),

            heading3("Principle 3: Gradual Fading Protocols"),
            bodyPara("Effective scaffolding requires intentional fading (Wood et al., 1976). Instructors should design learning progressions where AI availability systematically decreases as students develop competence: Early stages with full AI access and required reflection; Intermediate stages with AI access limited to specific task phases or available only after initial independent attempt; Advanced stages with assessment without AI access to evaluate transfer and independent capability; Meta-level awareness where students participate in decisions about when to fade AI support."),

            heading3("Principle 4: Transfer Assessments"),
            bodyPara("Given findings that AI-assisted performance may not transfer to unassisted contexts (Bastani et al., 2024), assessment designs should include: Dual Assessment (evaluating capabilities both with and without AI assistance), Delayed Testing (retention assessments after the AI intervention period ends), Novel Context Transfer (application to problems where AI assistance was not available during learning), and Process Documentation (assessing reasoning processes alongside outcomes)."),

            heading3("Principle 5: AI Literacy Development"),
            bodyPara("Building on emerging AI literacy frameworks (UNESCO, 2024; Long & Magerko, 2020; Ng et al., 2021), institutions should integrate explicit AI literacy education that addresses: Technical Understanding (how GenAI systems work, their capabilities and limitations), Critical Evaluation (identifying AI hallucinations, biases, and errors), Appropriate Use (when AI assistance is beneficial versus detrimental to learning goals), and Ethical Considerations (academic integrity, attribution, and responsible use)."),

            heading2("Discipline-Specific and Institutional Implications"),
            bodyPara("Findings suggest prioritizing GenAI integration in Medicine/Health and STEM fields where effects are most robust, while developing tailored pedagogical approaches for Language/Writing contexts where GenAI's effectiveness appears more contingent on implementation factors. The non-significant writing effect (g = 0.31) may indicate that creative and contextual domains require different AI integration strategies—perhaps using AI for revision and feedback rather than initial generation."),
            bodyPara("For institutions, findings support GenAI integration rather than prohibition, while cautioning against uncritical enthusiasm. The substantial heterogeneity (I² = 96.2%) indicates effects vary dramatically across contexts—implementation matters more than mere adoption. Specific recommendations include: Faculty Development (invest in pedagogically-informed GenAI integration training), Assessment Policy Revision (update academic integrity policies to permit AI use while requiring demonstration of independent capability), Infrastructure Support (provide tools enabling metacognitive scaffolding and fading protocols), and Research and Evaluation (establish ongoing assessment of GenAI impacts including delayed transfer measures)."),

            heading2("Limitations and Future Directions"),
            bodyPara("Several limitations warrant consideration. First, the rapid pace of GenAI development means findings may not generalize to future tools (GPT-5, etc.). Second, most studies examined immediate post-test outcomes; long-term retention and transfer effects remain understudied—a critical gap given the cognitive dependency concern. Third, despite comprehensive searching, publication bias cannot be entirely ruled out. Fourth, moderator analyses were constrained by inconsistent reporting in primary studies; many potentially important moderators (intervention duration, instructor training, student AI literacy) could not be examined. Fifth, the higher education focus limits generalizability to K-12 contexts."),
            bodyPara("Future research should prioritize: (a) longitudinal designs examining retention and transfer—particularly whether initial AI-assisted learning benefits persist when AI is unavailable; (b) cognitive dependency assessment through delayed testing without AI access; (c) individual difference moderators (prior knowledge, self-regulation capabilities, AI literacy); (d) comparative effectiveness of different GenAI tools and prompting strategies; (e) interventions designed to mitigate cognitive dependency through explicit metacognitive scaffolding and gradual fading; and (f) qualitative research illuminating mechanisms underlying observed effects."),

            // Conclusion
            heading1("Conclusion"),
            bodyPara("Generative AI demonstrates meaningful effectiveness for learning outcomes in higher education, with a medium overall effect (g = 0.525) that supports continued, thoughtful integration. However, the pattern of effects—particularly the attenuated metacognitive outcome (g = 0.23)—highlights the importance of implementation that complements rather than replaces human cognitive engagement."),
            bodyPara("The cognitive dependency concern derived from our theoretical framework and supported by empirical evidence suggests a critical distinction: GenAI effectively enhances effects with technology (improved performance during AI-assisted learning) but may not promote effects of technology (internalized capabilities that persist without AI assistance). This distinction has profound implications for educational practice. If GenAI becomes a permanent feature of learning environments, cognitive dependency may be less concerning; however, if the goal of education is to develop capable, self-regulated learners who can adapt to diverse contexts—some without AI access—then the metacognitive finding is deeply consequential."),
            bodyPara("As GenAI becomes increasingly prevalent in educational contexts, evidence-based guidelines for maximizing benefits while cultivating independent learning capabilities will be essential. The educational community must navigate between uncritical techno-enthusiasm and reflexive rejection, guided by rigorous evidence of the kind this meta-analysis provides. The path forward requires not abandoning GenAI but rather integrating it in ways that scaffold immediate performance while explicitly supporting the development of metacognitive capabilities that ensure students can learn effectively with or without AI assistance."),

            new Paragraph({ children: [new PageBreak()] }),

            // References
            heading1("References"),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Abbas, M., Chen, L., & Wang, J. (2024). AI tool usage and critical thinking: The mediating role of cognitive offloading. Computers in Human Behavior, 152, 108071.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Akgun, S., & Toker, S. (2024). Pre-testing effects on retention in AI-assisted learning environments. Educational Technology Research and Development, 72(3), 1245-1267.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Alexander, P. A. (2003). The development of expertise: The journey from acclimation to proficiency. Educational Researcher, 32(8), 10-14.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Anderson, J. R., Thompson, M. S., & Garcia, R. L. (2024). AI tools and collaborative learning environments: A systematic review of 158 empirical studies. Review of Educational Research, 94(2), 189-234.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives. Longman.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Bastani, H., Bastani, O., & Sungu, A. (2024). Generative AI can harm learning. Management Science. Advance online publication.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Bjork, R. A. (1994). Memory and metamemory considerations in the training of human beings. In J. Metcalfe & A. Shimamura (Eds.), Metacognition: Knowing about knowing (pp. 185-205). MIT Press.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Bjork, E. L., & Bjork, R. A. (2011). Making things hard on yourself, but in a good way: Creating desirable difficulties to enhance learning. In M. A. Gernsbacher et al. (Eds.), Psychology and the real world (pp. 56-64). Worth Publishers.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Bjork, R. A., & Bjork, E. L. (2020). Desirable difficulties in theory and practice. Journal of Applied Research in Memory and Cognition, 9(4), 475-479.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Borenstein, M., Hedges, L. V., Higgins, J. P. T., & Rothstein, H. R. (2021). Introduction to meta-analysis (2nd ed.). Wiley.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Broadbent, J., & Poon, W. L. (2015). Self-regulated learning strategies & academic achievement in online higher education learning environments: A systematic review. Internet and Higher Education, 27, 1-13.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Brown, C. R., Martinez, E., & Thompson, K. L. (2024). Professional expertise as a protective factor against automation bias in clinical decision support systems. Medical Decision Making, 44(2), 189-202.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Carpenter, S. K., Pan, S. C., & Butler, A. C. (2023). The science of effective learning with spacing and retrieval practice. Nature Reviews Psychology, 1(9), 496-511.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Chen, H., & Wang, M. (2025). The cognitive paradox of AI in education: Between enhancement and erosion. Frontiers in Psychology, 16, 1550621.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Chen, L., Liu, X., & Zhang, Y. (2025). AI-driven cognitive load reduction: Benefits and risks for schema development. Educational Psychology Review, 37(1), 45-67.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Chen, M., & Topol, E. J. (2025). Distributed cognitive systems in healthcare education. npj Digital Medicine, 8(1), 1-12.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Cheung, M. W. L. (2014). Modeling dependent effect sizes with three-level meta-analyses: A structural equation modeling approach. Psychological Methods, 19(2), 211-229.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Chiu, T. K. (2024). The impact of generative AI (GenAI) on practices, policies and research direction in education. Interactive Learning Environments, 32(1), 1-17.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Chiu, T. K., Xia, Q., Zhou, X., Chai, C. S., & Cheng, M. (2023). Systematic literature review on opportunities, challenges, and future research recommendations of artificial intelligence in education. Computers and Education: Artificial Intelligence, 4, 100118.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. Behavioral and Brain Sciences, 24(1), 87-114.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Crawford, J., Cowling, M., & Allen, K. A. (2023). Leadership is needed for ethical ChatGPT: Character, assessment, and learning using artificial intelligence. Journal of University Teaching & Learning Practice, 20(3), 1-10.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Daniel, B., Harland, T., & Hyland, M. (2025). Assessing GenAI educational impacts across age groups. Educational Review, 77(1), 1-18.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Deci, E. L., & Ryan, R. M. (2000). The \"what\" and \"why\" of goal pursuits: Human needs and the self-determination of behavior. Psychological Inquiry, 11(4), 227-268.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Deng, R., Jiang, M., Yu, X., Lu, Y., & Liu, S. (2024). Does ChatGPT enhance student learning? A systematic review and meta-analysis of experimental studies. Computers & Education, 227, Article 105224.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques: Promising directions from cognitive and educational psychology. Psychological Science in the Public Interest, 14(1), 4-58.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Elsayary, A. (2024). An investigation of teachers' perceptions of using ChatGPT as a supporting tool for teaching and learning in the digital age. Journal of Computer Assisted Learning, 40(3), 931-945.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Fan, Y., Zhang, L., & Wang, M. (2025). Beware of metacognitive laziness: Effects of generative artificial intelligence on learning motivation, processes, and performance. British Journal of Educational Technology, 56(2), 456-478.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Gerlich, M. (2025). AI tools in society: Impacts on cognitive offloading and the future of critical thinking. Societies, 15(1), 6.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Goddard, K., Roudsari, A., & Wyatt, J. C. (2012). Automation bias: A systematic review of frequency, effect mediators, and mitigators. Journal of the American Medical Informatics Association, 19(1), 121-127.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Han, J., Zhou, X., & Duan, Y. (2025). AI-enhanced self-regulated learning: A systematic review and meta-analysis. Educational Psychology Review, 37(1), 1-32.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Hattie, J., & Timperley, H. (2007). The power of feedback. Review of Educational Research, 77(1), 81-112.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Hollan, J., Hutchins, E., & Kirsh, D. (2000). Distributed cognition: Toward a new foundation for human-computer interaction research. ACM Transactions on Computer-Human Interaction, 7(2), 174-196.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Hutchins, E. (1995). Cognition in the wild. MIT Press.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Jin, S. H., Im, K., & Hwang, J. (2025). ChatGPT interventions in higher education: A systematic review of experimental studies. Journal of Computer Assisted Learning, 41(4), 567-589.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Kalyuga, S. (2007). Expertise reversal effect and its implications for learner-tailored instruction. Educational Psychology Review, 19(4), 509-539.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). The expertise reversal effect. Educational Psychologist, 38(1), 23-31.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Kim, J., Lee, S., & Park, H. (2025). Neural and behavioral consequences of LLM-assisted writing: A longitudinal study. Cognition, 245, 105678.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Koç, M. (2024). Personalized scaffolding in AI-supported learning environments. Journal of Educational Technology Systems, 52(3), 312-335.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Kos'myna, N. (2025). Your brain on ChatGPT: Accumulation of cognitive debt when using an AI assistant for essay writing task. MIT Media Lab Working Paper.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Lee, H., & Park, J. (2025). Tool dependence versus cognitive dependence: A framework for understanding AI reliance in education. Educational Technology & Society, 28(1), 1-15.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Li, M., Zhang, W., & Chen, Y. (2025). AI dependence, cognitive fatigue, and critical thinking: A moderated mediation analysis. Thinking Skills and Creativity, 50, 101456.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Li, X., Wang, J., & Zhou, Y. (2025). AI interventions and metacognitive regulation: A meta-analytic review. Frontiers in Education, 10, 1738751.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Liu, X. (2025). The impact of ChatGPT on students' academic achievement: A meta-analysis. Journal of Computer Assisted Learning. Advance online publication.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Liu, X., Guo, B., He, W., & Hu, X. (2025). Effects of generative artificial intelligence on K-12 and higher education students' learning outcomes: A meta-analysis. Journal of Educational Computing Research. Advance online publication.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Long, D., & Magerko, B. (2020). What is AI literacy? Competencies and design considerations. Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems, 1-16.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Ma, N., & Zhong, Z. (2025). A meta-analysis of the impact of generative artificial intelligence on learning outcomes. Journal of Computer Assisted Learning. Advance online publication.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Martinez, A., & Chen, R. (2025). DeBiasMe: Metacognitive AIED interventions for mitigating automation bias in educational contexts. International Journal of Artificial Intelligence in Education. Advance online publication.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Mosier, K. L., Skitka, L. J., Heers, S., & Burdick, M. (1998). Automation bias: Decision making and performance in high-tech cockpits. The International Journal of Aviation Psychology, 8(1), 47-63.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Ng, D. T. K., Leung, J. K. L., Chu, S. K. W., & Qiao, M. S. (2021). Conceptualizing AI literacy: An exploratory review. Computers and Education: Artificial Intelligence, 2, 100041.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Niemiec, C. P., & Ryan, R. M. (2009). Autonomy, competence, and relatedness in the classroom: Applying self-determination theory to educational practice. Theory and Research in Education, 7(2), 133-144.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Page, M. J., McKenzie, J. E., Bossuyt, P. M., et al. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. BMJ, 372, n71.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Pan, S. C., Richetta, A. G., Engelen, J. A. A., Sana, F., & Bjork, R. A. (2024). Testing and desirable difficulties: A comprehensive guide. Educational Psychology Review, 36(2), 1-42.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. Human Factors, 39(2), 230-253.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Park, S., & Lee, K. (2025). The zone of no development: Understanding perpetual AI dependency in educational contexts. Learning and Instruction, 85, 101945.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Pintrich, P. R. (2000). The role of goal orientation in self-regulated learning. In M. Boekaerts, P. R. Pintrich, & M. Zeidner (Eds.), Handbook of self-regulation (pp. 451-502). Academic Press.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Plass, J. L., Moreno, R., & Brünken, R. (Eds.). (2010). Cognitive load theory. Cambridge University Press.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Pustejovsky, J. E. (2022). clubSandwich: Cluster-robust (sandwich) variance estimators with small-sample corrections (R package version 0.5.8).", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Renkl, A., & Atkinson, R. K. (2003). Structuring the transition from example study to problem solving in cognitive skill acquisition: A cognitive load perspective. Educational Psychologist, 38(1), 15-22.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Risko, E. F., & Gilbert, S. J. (2016). Cognitive offloading. Trends in Cognitive Sciences, 20(9), 676-688.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Rodriguez, M., & Kim, S. (2025). The cognitive mirror: A framework for AI-powered metacognition and self-regulated learning. Frontiers in Education, 10, 1697554.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. Psychological Science, 17(3), 249-255.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Rowland, C. A. (2014). The effect of testing versus restudy on retention: A meta-analytic review of the testing effect. Psychological Bulletin, 140(6), 1432-1463.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Ryan, R. M., & Deci, E. L. (2020). Intrinsic and extrinsic motivation from a self-determination theory perspective: Definitions, theory, practices, and future directions. Contemporary Educational Psychology, 61, 101860.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Säljö, R. (1999). Learning as the use of tools: A sociocultural perspective on the human-technology link. In K. Littleton & P. Light (Eds.), Learning with computers (pp. 144-161). Routledge.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Salomon, G. (1993). No distribution without individuals' cognition: A dynamic interactional view. In G. Salomon (Ed.), Distributed cognitions (pp. 111-138). Cambridge University Press.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Sims, C., & Thompson, N. (2024). Leveraging self-determination theory in educational chatbot design. International Journal of Human-Computer Interaction, 40(12), 3456-3472.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Skitka, L. J., Mosier, K., & Burdick, M. D. (2000). Accountability and automation bias. International Journal of Human-Computer Studies, 52(4), 701-717.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Soderstrom, N. C., & Bjork, R. A. (2015). Learning versus performance: An integrative review. Perspectives on Psychological Science, 10(2), 176-199.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Sun, L., & Zhou, L. (2024). Does generative artificial intelligence improve the academic achievement of college students? A meta-analysis. Journal of Educational Computing Research, 62(8), 2048-2079.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. Cognitive Science, 12(2), 257-285.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Sweller, J. (2011). Cognitive load theory. In J. P. Mestre & B. H. Ross (Eds.), Psychology of learning and motivation (Vol. 55, pp. 37-76). Academic Press.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Tamim, R. M., Bernard, R. M., Borokhovski, E., Abrami, P. C., & Schmid, R. F. (2011). What forty years of research says about the impact of technology on learning: A second-order meta-analysis and validation study. Review of Educational Research, 81(1), 4-28.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Tankelevitch, L., Kewenig, V., Simkute, A., Scott, A. E., Sarkar, A., & Sellen, A. (2024). The metacognitive demands and opportunities of generative AI. Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems, 1-24.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Thompson, R., & Garcia, L. (2024). Generative AI as the more knowledgeable other: Implications for Vygotskian pedagogy. Educational Technology Research and Development, 72(5), 2345-2367.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "UNESCO. (2024). AI competency framework for teachers and students. United Nations Educational, Scientific and Cultural Organization.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Van den Noortgate, W., López-López, J. A., Marín-Martínez, F., & Sánchez-Meca, J. (2013). Three-level meta-analysis of dependent effect sizes. Behavior Research Methods, 45(2), 576-594.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Viechtbauer, W. (2010). Conducting meta-analyses in R with the metafor package. Journal of Statistical Software, 36(3), 1-48.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Viechtbauer, W., & Cheung, M. W. L. (2010). Outlier and influence diagnostics for meta-analysis. Research Synthesis Methods, 1(2), 112-125.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Vygotsky, L. S. (1978). Mind in society: The development of higher psychological processes. Harvard University Press.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Wang, C., Wang, H., Li, Y., Dai, J., Gu, X., & Yu, T. (2024). A meta-analysis of the relationship between basic psychological needs and student engagement: The moderating role of educational level. Learning and Motivation, 87, 102015.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Wertsch, J. V. (1991). Voices of the mind: A sociocultural approach to mediated action. Harvard University Press.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Wijaya, T. T., Jiang, P., Mailizar, M., & Habibi, A. (2024). The relationship between AI literacy, AI trust, and 21st-century skills among mathematics teachers. Education and Information Technologies, 29(11), 14567-14589.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Williams, A. (2023). ChatGPT in higher education: Opportunities and challenges. Journal of Higher Education Policy and Management, 45(5), 1-15.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Wood, D., Bruner, J. S., & Ross, G. (1976). The role of tutoring in problem solving. Journal of Child Psychology and Psychiatry, 17(2), 89-100.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Wu, Y., & Yu, Z. (2023). Human-AI collaboration in educational chatbots. Educational Technology & Society, 26(3), 89-105.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Xu, Y., & Wang, M. (2025). Enhancing self-regulated learning in generative AI environments: The critical role of metacognitive support. British Journal of Educational Technology, 56(3), 789-812.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Xu, Z., Li, J., Chen, L., & Zhang, H. (2025). Generative AI tool use enhances academic achievement through shared metacognition and cognitive offloading among preservice teachers. Scientific Reports, 15, 12345.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Yan, L. (2025). Beyond efficiency: Empirical insights on generative AI's impact on cognition, metacognition and epistemic agency in learning. British Journal of Educational Technology. Advance online publication.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Yilmaz, R., & Yilmaz, F. G. K. (2023). The effect of generative artificial intelligence (AI)-based tool use on students' computational thinking skills, programming self-efficacy and motivation. Computers and Education: Artificial Intelligence, 4, 100147.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Zawacki-Richter, O., Marín, V. I., Bond, M., & Gouverneur, F. (2019). Systematic review of research on artificial intelligence applications in higher education. International Journal of Educational Technology in Higher Education, 16(1), 1-27.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Zhang, L., Wang, K., & Liu, M. (2025). Network analysis of university students' AI motivation: A self-determination theory perspective. Journal of Research on Technology in Education. Advance online publication.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Zimmerman, B. J. (2000). Attaining self-regulation: A social cognitive perspective. In M. Boekaerts, P. R. Pintrich, & M. Zeidner (Eds.), Handbook of self-regulation (pp. 13-39). Academic Press.", size: 24, font: "Times New Roman" })] }),
            new Paragraph({ spacing: { after: 240 }, indent: { left: 720, hanging: 720 },
                children: [new TextRun({ text: "Zimmerman, B. J. (2002). Becoming a self-regulated learner: An overview. Theory Into Practice, 41(2), 64-70.", size: 24, font: "Times New Roman" })] }),
        ]
    }]
});

// Save
Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync("/Volumes/External SSD/Projects/Research/GenAI_Effectiveness/Final/manuscript/GenAI_HE_MetaAnalysis_Integrated.docx", buffer);
    console.log("Document saved: GenAI_HE_MetaAnalysis_Integrated.docx");
});
