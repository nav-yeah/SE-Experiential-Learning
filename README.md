# Software Engineering Experiential Learning

This repository contains the lab submissions for the Software Engineering course at PES University.

## Labs

### Lab 1: Requirements Engineering and UML Use-Case Modelling
Developed requirements documentation and UML use-case models for a **Community Lost & Found Matching Network**.

**Key Deliverables:**
- Functional and non-functional requirements with priorities and acceptance criteria.
- UML use-case diagram.
- Detailed use-case flow specification for claiming a found item, including alternate flows, exceptions, and verification rules.

**Concepts:** Requirements engineering, acceptance criteria, UML modelling, use-case specifications, and security requirements.

### Lab 2: Agile Planning and Sprint Tracking
Applied Agile project-management practices to organise development work for the Community Lost & Found Matching Network.

**Key Deliverables:**
- Epics and prioritised user stories.
- Story-point estimates and sprint planning.
- Sprint boards, burndown charts, and dashboard views.
- Reflections on sprint progress and estimation accuracy.

**Concepts:** Agile methodology, backlog management, sprint planning, story-point estimation, and progress tracking.

### Lab 3: Software Architecture Selection and Justification
Designed and justified a layered architecture for the Community Lost & Found Matching Network.

**Key Deliverables:**
- Written architecture justification.
- UML architecture diagram.

**Key Design Considerations:**
- Separation of presentation, business logic, and data access.
- Data consistency and claim verification.
- Security boundaries and protection of user information.
- Performance considerations for item matching.

**Concepts:** Software architecture, layered design, separation of concerns, scalability, and architectural trade-offs.

### Lab 4: AI-Assisted Debugging and Feature Enhancement
Used Python, Pygame, and an LLM-assisted development workflow to debug and enhance a Simon-style Memory Color Pattern game.

**Key Enhancements:**
- Fixed sequence duplication between rounds.
- Implemented progressively faster sequence playback.
- Added colour-specific sound effects.
- Introduced a countdown timer for player input.

**Key Deliverables:**
- Python source code.
- Before-and-after gameplay recordings.
- LLM conversation history documenting the debugging and development process.

**Concepts:** Python programming, Pygame, state machines, debugging, time-based logic, adaptive difficulty, and AI-assisted software development.

### Lab 5: Static Code Analysis

Applied static code analysis techniques to evaluate and improve the code quality, maintainability, and security of the **Support Ticket Tracker** project.

**Key Activities:**
- Analysed the codebase using **Bandit, Flake8, and Pylint** to identify potential security issues, coding standard violations, and code quality concerns.
- Examined and documented static analysis findings.
- Applied code improvements based on the identified issues.
- Compared before-and-after analysis results to assess code quality improvements.

**Key Deliverables:**
- Static analysis reports and findings.
- Before-and-after analysis outputs.
- Documentation of identified issues and improvements.
- Updated project code and supporting lab documentation.

**Concepts:** Static code analysis, software quality assurance, secure coding practices, linting, code maintainability, technical debt, and automated quality checks.

### Lab 6: Code Coverage and Branch Coverage Testing

Applied code coverage and branch coverage testing techniques to evaluate the testing effectiveness of the **Restaurant Bill** application.

**Key Activities:**
- Developed unit test cases for the application's bill calculation, bill splitting, and table waiting functionalities using **pytest**.
- Measured statement coverage and branch coverage using **Coverage.py**.
- Designed test cases to exercise different conditional branches, including valid inputs, invalid inputs, and boundary conditions.
- Analysed coverage reports to identify untested statements and branches.

**Key Deliverables:**
- `restaurant_bill.py` — Application source code.
- `CodeCoverageTest_58_application.py` — Code coverage test cases.
- `BranchCoverageTest_58_application.py` — Branch coverage test cases.
- Code coverage and branch coverage screenshots.

**Results:**
- 100% statement coverage.
- 100% branch coverage (22/22 branches).

**Concepts:** Software testing, unit testing, statement coverage, branch coverage, test adequacy, pytest, and Coverage.py.

### Lab 7: Fuzzing for Input Validation Bugs

Applied property-based testing and fuzz testing techniques to identify and fix input validation bugs in the **Restaurant Bill Parser** application.

**Key Activities:**
- Used the **Hypothesis** library to automatically generate a wide range of test inputs, including unexpected and invalid values.
- Tested the robustness of `clean_dish_name()`, `parse_item_prices()`, and `split_amount()` functions.
- Identified input-handling issues that caused runtime exceptions.
- Implemented defensive input validation and error handling to prevent unexpected crashes.
- Re-ran property-based tests to verify the fixes.

**Key Deliverables:**
- `restaurant_bill_parser.py` — Updated parser with input validation and error handling.
- `test_restaurant_bill_parser.py` — Hypothesis-based property testing test cases.
- `SRN_NAME_LAB7.pdf` — Screenshots documenting the testing process and reflection answers.

**Concepts:** Fuzz testing, property-based testing, input validation, defensive programming, exception handling, Hypothesis, and software robustness.

## Technologies and Concepts

- UML and software modelling
- Requirements engineering
- Agile project management
- Software architecture and design
- Python and Pygame
- AI-assisted debugging and development
- Static code analysis and software quality assurance
- Bandit, Flake8, and Pylint
- Secure coding practices and code quality improvement
- Unit testing and test coverage
- Statement coverage and branch coverage
- pytest and Coverage.py
- Fuzz testing and property-based testing
- Hypothesis and input validation

## Repository Structure

- `Lab1/` — Requirements engineering and use-case modelling
- `Lab2/` — Agile planning and sprint tracking
- `Lab3/` — Architecture design and justification
- `Lab4/` — AI-assisted debugging and game enhancement
- `Lab5/` — Static code analysis, code quality assessment, and improvement
- `Lab6/` — Code coverage and branch coverage testing
- `Lab7/` — Fuzz testing and input validation using Hypothesis
