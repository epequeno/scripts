" better plugin management
call pathogen#infect()

" stupid swap files
set nobackup
set nowritebackup
set noswapfile

" Force save files that require root
cmap w!! %!sudo tee > /dev/null %

" Better color scheme
set background=dark

" Line Numbers
set number

" Show <Leader> and command at bottom-right of screeen
set showcmd

" Search stuff
" Highlight things that we find with the search
set hlsearch
set incsearch
set ignorecase
set smartcase

" Spaces instead of tabs
set expandtab

" Python stuff
filetype indent plugin on
syntax enable
" Smart indenting
set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class
set tabstop=8 
set shiftwidth=4 
set softtabstop=4
:let python_version_2=1
:let python_highlight_all=1
set textwidth=79 " 80 char width
set nowrap " don't wrap text on load
set colorcolumn=80
highlight ColorColoumn ctermbg=233

" Fix wierd apple backspace thing
set nocompatible
set backspace=2

" =========================== Maps ======================================
" remap leader to ,
let mapleader = ","

" Make basic function definition  (PYTHON)
:map <Leader>f idef foo():<Return>pass

" =======================================================================
