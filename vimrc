" Better color scheme
set background=dark

" Line Numbers
set number

" Show <Leader> and command at bottom-right of screeen
set showcmd

" Highlight things that we find with the search
set hlsearch

" Spaces instead of tabs
set expandtab
set autoindent

" Python stuff
filetype indent plugin on
syntax enable
set tabstop=8 
set shiftwidth=4 
set softtabstop=4

" =========================== Maps ======================================
" Default leader is \

" Make basic function definition  (PYTHON)
:map <Leader>d idef foo():<Return><Tab>

" =======================================================================
