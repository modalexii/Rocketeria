/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For complete reference see:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config
	 CKEDITOR.stylesSet.add( 'my_styles', [
		// Inline styles
		{ name: 'Undecorate Link',
			element: 'a', 
			styles: { 'text-decoration':'none;'}
		},
		{ name: 'Big', element: 'big', },
		{ name: 'Quote Feed',
			element: 'span', 
			attributes: { 'class': 'quote_feed' }
		},
		{ name: 'Highlight: R', element: 'span', styles: { 'background-color': '#f97b7d' } },
		{ name: 'Highlight: G', element: 'span', styles: { 'background-color': '#9df860' } },
		{ name: 'Highlight: B', element: 'span', styles: { 'background-color': '#abfffc' } },
		{ name: 'Highlight: Y', element: 'span', styles: { 'background-color': '#f5ed14' } },
		{ name: 'Highlight: P', element: 'span', styles: { 'background-color': '#e26ffb' } },
		{ name: 'Button: R',
			element: 'span', 
			attributes: { 'class': 'btn' },
			styles: { 'color':'#fff', 'background-color':'#96231f' }
		},
		{ name: 'Button: G',
			element: 'a', 
			attributes: { 'class': 'btn' },
			styles: { 'background-color':'#58a326' }
		},
		{ name: 'Button: B',
			element: 'a', 
			attributes: { 'class': 'btn' },
			styles: { 'background-color':'#04bde5' }
		},
		{ name: 'Button: Y',
			element: 'a', 
			attributes: { 'class': 'btn' },
			styles: { 'background-color':'#d79e05' }
		},
		{ name: 'Button: P',
			element: 'a', 
			attributes: { 'class': 'btn' },
			styles: { 'background-color':'#9702b7' }
		},
		// Block-level styles
		{ 
			name: 'Testimonial',
			element: 'p',
			styles: { 'border-bottom':'1px solid #0f0403', 'padding-bottom':'12px', 'padding-top':'12px' },
			attributes: { 'class': 'testimonial' }
		}
	] );

	config.stylesSet = 'my_styles';

	// The toolbar groups arrangement, optimized for two toolbar rows.
	config.toolbarGroups = [
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'forms' },
		{ name: 'tools' },
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'others' },
		'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
		{ name: 'styles' },
		{ name: 'colors' },
		{ name: 'about' }
	];

	// Remove some buttons provided by the standard plugins, which are
	// not needed in the Standard(s) toolbar.
	config.removeButtons = 'Underline,Subscript,Superscript';

	// Set the most common block elements.
	config.format_tags = 'p;h1;h2;h3;pre';

	// Simplify the dialog windows.
	config.removeDialogTabs = 'image:advanced;link:advanced';
};
