// ASMA-OS specification and operational report template
#set page(paper: "a4", margin: (x: 22mm, y: 20mm))
#set text(font: "Inter", size: 10pt, fill: rgb("101B2D"))
#set heading(numbering: "1.")
#set par(leading: 0.7em, justify: true)

#let report_title = sys.inputs.at("title", default: "ASMA-OS System Report")
#let report_version = sys.inputs.at("version", default: "6.0")
#let report_summary = sys.inputs.at("summary", default: "Specification overview unavailable.")

#align(center)[
  #text(size: 24pt, weight: "bold", fill: rgb("101B2D"))[ASMA-OS]
  #v(4pt)
  #text(size: 11pt, fill: rgb("718096"))[Unified Autonomous Execution Operating System]
  #v(18pt)
  #text(size: 18pt, weight: "semibold")[#report_title]
  #v(4pt)
  #text(fill: rgb("718096"))[Specification version #report_version]
]

#line(length: 100%, stroke: rgb("35C6D8", 1.2pt))
#v(12pt)

= System Overview
#report_summary

#show heading.where(level: 1): it => block(above: 14pt, below: 6pt)[
  #text(fill: rgb("101B2D"), weight: "bold")[#it]
]

#let status(value) = {
  let color = if value == "PASSED" { rgb("42B883") }
    else if value == "FAILED" { rgb("D95D5D") }
    else { rgb("F2B84B") }
  text(fill: color, weight: "bold")[#value]
}

// Include report sections with = headings and provide content at compilation.
#v(1fr)
#line(length: 100%, stroke: rgb("20334D", 0.5pt))
#text(size: 8pt, fill: rgb("718096"))[ASMA-OS • System specification and operational report]
