import yaml
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

def generate_numbering_map():
    """
    Parses _quarto.yml to create and return a mapping of chapter files
    to their desired hierarchical numbers.
    """
    quarto_yml_path = Path('_quarto.yml')
    if not quarto_yml_path.exists():
        print("Error: _quarto.yml not found.")
        return None

    with open(quarto_yml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    chapters_list = config.get('book', {}).get('chapters', [])
    mapping = {}
    chapter_counter = 0

    for item in chapters_list:
        if isinstance(item, str):
            if Path(item).stem.lower() not in ['index', 'preface', 'about']:
                chapter_counter += 1
                html_file = Path(item).with_suffix('.html').as_posix()
                mapping[html_file] = f"{chapter_counter}"
        
        elif isinstance(item, dict) and 'part' in item:
            chapter_counter += 1 # A part starts a new chapter number
            part_chapters = item.get('chapters', [])
            sub_chapter_counter = 1
            for sub_chapter in part_chapters:
                html_file = Path(sub_chapter).with_suffix('.html').as_posix()
                mapping[html_file] = f"{chapter_counter}.{sub_chapter_counter}"
                sub_chapter_counter += 1
    
    print("Successfully generated numbering map in memory:")
    import json
    print(json.dumps(mapping, indent=2))
    return mapping

def post_process_html(numbering_map):
    """
    Parses all HTML files in the _book directory to fix chapter, section,
    and figure numbering based on the provided numbering_map.
    """
    book_dir = Path('_book')
    book_dir_abs = book_dir.resolve()
    print("Starting post-processing of HTML files...")

    for file_path in book_dir.rglob('*.html'):
        relative_path_posix = file_path.relative_to(book_dir).as_posix()
        print(f"Processing {relative_path_posix}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml')

        # Universal Sidebar and Nav Renumbering (applied to every page)
        for link in soup.select('#quarto-sidebar .sidebar-item-container > a.sidebar-link, .nav-page-previous a.pagination-link, .nav-page-next a.pagination-link'):
            href = link.get('href')
            if href and not href.startswith(('http://', 'https://', '#')):
                # Resolve the path relative to the current file's directory
                try:
                    target_abs = (file_path.parent / href).resolve(strict=False)
                    target_rel_posix = target_abs.relative_to(book_dir_abs).as_posix()
                    # Remove fragment for map lookup
                    lookup_key = target_rel_posix.split('#')[0]

                    if lookup_key in numbering_map:
                        number_span = link.select_one('.chapter-number')
                        title_span = link.select_one('.chapter-title')
                        if number_span:
                            number_span.string = numbering_map[lookup_key]
                        # For items without a number (like Preface), ensure they don't get one
                        elif title_span and lookup_key not in numbering_map:
                            if link.select_one('.chapter-number'):
                                link.select_one('.chapter-number').decompose()
                except ValueError:
                    # This can happen if the link points outside the book directory, e.g. `../index.html` from a top-level file
                    print(f"  -> Skipping link with path pointing outside the book directory: {href}")
                    continue


        # Page-Specific Renumbering 
        correct_number = numbering_map.get(relative_path_posix)
        if not correct_number:
            print(f"  -> No numbering entry found. Skipping page-specific changes.")
            # Clean up title number if it's not supposed to have one
            main_title_span = soup.select_one('#quarto-document-content h1.title .chapter-number')
            if main_title_span:
                main_title_span.decompose()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            continue


        # Determine the incorrect number from the first section found
        first_section = soup.select_one('section[data-number]')
        incorrect_number = None
        if first_section:
            incorrect_number = first_section['data-number'].split('.')[0]

        # Fallback for pages with no sections but with a numbered title
        if not incorrect_number:
            main_title = soup.select_one('h1.title[data-number]')
            if main_title:
                incorrect_number = main_title['data-number'].split('.')[0]
        
        # Fallback to browser title if all else fails
        if not incorrect_number and soup.title and soup.title.string:
            title_match = re.match(r'^(\d+)', soup.title.string.strip())
            if title_match:
                incorrect_number = title_match.group(1)


        if not incorrect_number:
            print(f"  -> Could not determine original chapter number. Skipping page-specific changes.")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            continue
        
        print(f"  -> Rewriting numbers from '{incorrect_number}' to '{correct_number}'")
        
        incorrect_prefix = f"{incorrect_number}."
        correct_prefix = f"{correct_number}."

        # Update main H1 title and its data-number attribute
        main_title_h1 = soup.select_one('#quarto-document-content h1.title')
        if main_title_h1:
            # Update data-number on H1 tag itself
            if main_title_h1.has_attr('data-number'):
                 main_title_h1['data-number'] = correct_number
            # Update the visible chapter number span
            main_title_span = main_title_h1.select_one('.chapter-number')
            if main_title_span:
                main_title_span.string = correct_number
            else: # If the span doesn't exist, create it
                new_span = soup.new_tag("span", attrs={"class": "chapter-number"})
                new_span.string = correct_number
                main_title_h1.insert(0, new_span)
                # Add a non-breaking space for separation
                main_title_h1.insert(1, NavigableString('\xa0'))


        # Update browser <title> tag
        if soup.title and soup.title.string:
            # Use a regex that finds the number at the start of the string.
            # Handles "15 Title" and "15.1 Title".
            soup.title.string = re.sub(rf'^{re.escape(incorrect_number)}(?:\.[\d\.]+)*[\s\xa0]+', f'{correct_number}\xa0', soup.title.string)


        # Update ALL breadcrumb elements
        for breadcrumb_span in soup.select('.quarto-page-breadcrumbs .breadcrumb-item:last-child .chapter-number'):
            breadcrumb_span.string = correct_number

        # Update all sub-headings (and their parent sections) and their data-numbers
        for section in soup.select('section[data-number]'):
            original_data_number = section['data-number']
            if original_data_number.startswith(incorrect_prefix):
                # Replace only the first part of the number
                new_data_number = correct_prefix + '.'.join(original_data_number.split('.')[1:])
                section['data-number'] = new_data_number
                
                header = section.find(['h2','h3','h4','h5','h6'], recursive=False)
                if header:
                    header['data-number'] = new_data_number
                    number_span = header.select_one('.header-section-number')
                    if number_span:
                        number_span.string = new_data_number
        
        # Update right-hand Table of Contents
        for toc_item in soup.select('#TOC .nav-link'):
            # Update section numbers in the text
            number_span = toc_item.select_one('.header-section-number')
            if number_span and number_span.string and number_span.string.strip().startswith(incorrect_prefix):
                original_toc_number = number_span.string.strip()
                new_toc_number = correct_prefix + '.'.join(original_toc_number.split('.')[1:])
                number_span.string = new_toc_number

        # Update Figure, Table, and Listing captions
        for caption in soup.select('.quarto-float-caption'):
            # Find the text node that contains the caption label, e.g., "Figure 1.1:"
            caption_text_node = None
            for node in caption.contents:
                if isinstance(node, NavigableString) and node.strip():
                    caption_text_node = node
                    break

            if caption_text_node:
                original_text = str(caption_text_node).lstrip()
                # Regex to match "Figure 1.", "Table 1.", etc.
                new_text = re.sub(rf'^(Figure|Table|Listing)([\s\xa0]){re.escape(incorrect_number)}\.', rf'\g<1>\g<2>{correct_number}.', original_text)
                if new_text != original_text:
                    caption_text_node.replace_with(new_text)

        # Update Theorem-like environment titles (Theorem, Lemma, Example, etc.)
        for theorem_title in soup.select('.theorem-title strong'):
            original_text = theorem_title.get_text(strip=True)
            # Match patterns like "Theorem 25.2", "Example 25.1", etc.
            new_text = re.sub(
                rf'^(Theorem|Lemma|Corollary|Proposition|Conjecture|Definition|Example|Exercise|Solution|Remark|Algorithm)([\s\xa0]+){re.escape(incorrect_number)}\.',
                rf'\g<1>\g<2>{correct_number}.',
                original_text
            )
            if new_text != original_text:
                theorem_title.string = new_text

        # Update MathJax Equation Numbers in \tag{} and data-eq-number for inline equations
        # This must run BEFORE cross-reference updates to ensure the correct numbers are available.
        # For display equations
        for math_span in soup.select('span.math.display'):
            if math_span.string:
                original_latex = math_span.string
                # Regex to find \tag{1.x} and replace it with \tag{6.2.x}
                new_latex = re.sub(rf'(\\tag\{{){re.escape(incorrect_prefix)}([^\}}]+\}})', rf'\g<1>{correct_prefix}\g<2>', original_latex)
                if new_latex != original_latex:
                    math_span.string = new_latex
        
        # For inline equations
        for math_span in soup.select('span.math.inline[data-eq-number]'):
            original_eq_number = math_span['data-eq-number']
            if original_eq_number.startswith(incorrect_prefix):
                new_eq_number = correct_prefix + '.'.join(original_eq_number.split('.')[1:])
                math_span['data-eq-number'] = new_eq_number
                
                # Also update the visible text if it's being displayed, e.g. "(1.1)"
                next_sibling = math_span.find_next_sibling('span', class_='paren-eq-no')
                if next_sibling and next_sibling.string:
                    next_sibling.string = f"({new_eq_number})"

        # Update in-text cross-references (e.g., @fig-mylabel, @eq-mylabel)
        for xref in soup.select('a.quarto-xref'):
            href = xref.get('href')
            if not (href and href.startswith('#')):
                continue

            target_id = href[1:]
            target_element = soup.select_one(f'#{target_id}')
            if not target_element:
                continue

            # The text can be complex, e.g., "Figure <span>6.2.3</span>"
            # We get the full, stripped text of the <a> tag.
            current_text = xref.get_text(strip=True)
            if not current_text:
                continue

            # Split carefully to handle "Section 6.2" vs "Fig. 6.2.1"
            ref_parts = current_text.split(maxsplit=1)
            
            ref_type = None
            if len(ref_parts) == 2:
                ref_type = ref_parts[0]
            elif len(ref_parts) == 1:
                # Handle cases where the link text is just the number, e.g., "15.3"
                # Infer the type from the target element's ID prefix.
                if target_id.startswith('fig-'):
                    ref_type = 'Figure'
                elif target_id.startswith('tbl-'):
                    ref_type = 'Table'
                elif target_id.startswith('lst-'):
                    ref_type = 'Listing'
                elif target_id.startswith('sec-'):
                    ref_type = 'Section'
                elif target_id.startswith('eq-'):
                    # Use "Equation" for consistency with Quarto's output for this case
                    ref_type = 'Equation'
                elif target_id.startswith('thm-'):
                    ref_type = 'Theorem'
                elif target_id.startswith('lem-'):
                    ref_type = 'Lemma'
                elif target_id.startswith('cor-'):
                    ref_type = 'Corollary'
                elif target_id.startswith('prp-'):
                    ref_type = 'Proposition'
                elif target_id.startswith('cnj-'):
                    ref_type = 'Conjecture'
                elif target_id.startswith('def-'):
                    ref_type = 'Definition'
                elif target_id.startswith('exm-'):
                    ref_type = 'Example'
                elif target_id.startswith('exr-'):
                    ref_type = 'Exercise'
                elif target_id.startswith('sol-'):
                    ref_type = 'Solution'
                elif target_id.startswith('rem-'):
                    ref_type = 'Remark'
                elif target_id.startswith('alg-'):
                    ref_type = 'Algorithm'
            
            if not ref_type:
                continue

            correct_target_number = None

            # Find number for sections/headers
            if target_element.has_attr('data-number'):
                correct_target_number = target_element['data-number']

            # Find number for figures/tables
            elif 'quarto-float' in target_element.get('class', []):
                caption = target_element.select_one('.quarto-float-caption')
                if caption:
                    caption_text = caption.get_text().strip()
                    # Extract the full number (e.g., "6.2.1") from the corrected caption
                    match = re.search(rf'^(?:Figure|Table|Listing)[\s\xa0]+({re.escape(correct_number)}\.\d+)', caption_text)
                    if match:
                        correct_target_number = match.group(1)

            # Find number for theorem-like environments (Theorem, Lemma, Example, etc.)
            elif 'theorem' in target_element.get('class', []):
                theorem_title = target_element.select_one('.theorem-title strong')
                if theorem_title:
                    title_text = theorem_title.get_text(strip=True)
                    # Extract number from patterns like "Theorem 25.2", "Example 25.1", etc.
                    match = re.search(rf'^(?:Theorem|Lemma|Corollary|Proposition|Conjecture|Definition|Example|Exercise|Solution|Remark|Algorithm)[\s\xa0]+({re.escape(correct_number)}\.\d+)', title_text)
                    if match:
                        correct_target_number = match.group(1)

            # Find number for equations
            else:
                # The target_element is the container span (e.g., <span id="eq-something">)
                # The actual equation number is in a child span with class 'math' and a data-eq-number
                math_span = target_element.select_one('span.math[data-eq-number]')
                if math_span:
                    correct_target_number = math_span.get('data-eq-number')
                else: # Fallback for display equations with a <tag>
                    math_display_span = target_element.select_one('span.math.display')
                    if math_display_span and math_display_span.string:
                        # The number is inside the LaTeX \tag{}
                        tag_match = re.search(r'\\tag\{([^}]+)\}', math_display_span.string)
                        if tag_match:
                            correct_target_number = tag_match.group(1)
                    else: # Fallback for older structures if needed
                        tag_span = target_element.select_one('.tag')
                        if tag_span and tag_span.string:
                            raw_tag = tag_span.string.strip('()')
                            if raw_tag.startswith(incorrect_prefix):
                                 correct_target_number = correct_prefix + '.'.join(raw_tag.split('.')[1:])
                            else:
                                 correct_target_number = raw_tag


            if correct_target_number:
                # Handle different structures of xref links
                number_span = xref.select_one('span')
                if number_span:
                    # Case: <a>Equation&nbsp;<span>15.8</span></a>
                    current_number = number_span.get_text(strip=True)
                    if current_number != correct_target_number:
                        print(f"  -> Correcting internal xref number: '{current_number}' -> '{correct_target_number}'")
                        number_span.string = correct_target_number
                else:
                    # Case: <a>Section 15.2</a> or other simple text content
                    new_text = f"{ref_type}\xa0{correct_target_number}"
                    if current_text != new_text:
                        print(f"  -> Correcting internal xref: '{current_text}' -> '{new_text}'")
                        # Replace the entire content of the <a> tag
                        xref.clear()
                        xref.string = new_text
        
        # Final sweep for plain-text references.
        main_content = soup.select_one('#quarto-document-content')
        if main_content:
            # This regex finds numbers that start with the incorrect chapter number, e.g., "15.3", "15.3.1"
            number_pattern = re.compile(rf'^{re.escape(incorrect_number)}\.[\d\.]*$')
            keywords = ['Figure', 'Table', 'Listing', 'Section', 'Equation', 'Eq.',
                       'Theorem', 'Lemma', 'Corollary', 'Proposition', 'Conjecture',
                       'Definition', 'Example', 'Exercise', 'Solution', 'Remark', 'Algorithm']

            # PASS 1: Handle split elements like "Figure <span>15.3</span>"
            # Find all text nodes that are not in excluded tags
            text_nodes = main_content.find_all(string=lambda t: not t.find_parent(['a', 'pre', 'code', 'script', 'style', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', '.quarto-float-caption', '.tag', 'title']))

            for text_node in text_nodes:
                # Check if this text node ends with a keyword (possibly with whitespace)
                stripped_text = str(text_node).rstrip()
                if any(stripped_text.endswith(kw) for kw in keywords):
                    target_node = None
                    next_elem = text_node.next_sibling

                    if next_elem and next_elem.name == 'span' and next_elem.string:
                        # Case: Figure <span>15.3</span>
                        target_node = next_elem.string
                    
                    if target_node:
                        number_text = target_node.strip()
                        if number_pattern.match(number_text):
                            new_number = correct_prefix + '.'.join(number_text.split('.')[1:])
                            if number_text != new_number:
                                print(f"  -> Correcting plain text (split node): '{number_text}' -> '{new_number}'")
                                target_node.replace_with(new_number)

            # PASS 2: Handle combined text nodes like "Figure 15.3"
            keyword_and_number_pattern = re.compile(
                rf'(?P<keyword>{"|".join(keywords)})'
                rf'(?P<space>[\s\xa0]+)'
                rf'(?P<number>{re.escape(incorrect_number)}\.[\d\.]*)'
            )
            # Re-find text nodes as they might have been modified
            text_nodes = main_content.find_all(string=lambda t: not t.find_parent(['a', 'pre', 'code', 'script', 'style', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', '.quarto-float-caption', '.tag', 'title', 'span']))
            for text_node in text_nodes:
                original_text = str(text_node)
                
                def replacer(m):
                    number = m.group('number')
                    new_number = correct_prefix + '.'.join(number.split('.')[1:])
                    if number != new_number:
                        print(f"  -> Correcting plain text (single node): '{number}' -> '{new_number}'")
                        return m.group('keyword') + m.group('space') + new_number
                    return m.group(0)

                modified_text = keyword_and_number_pattern.sub(replacer, original_text)

                if modified_text != original_text:
                    text_node.replace_with(modified_text)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

if __name__ == "__main__":
    numbering_map = generate_numbering_map()
    if numbering_map is not None:
        post_process_html(numbering_map)
        print("Post-processing complete.")