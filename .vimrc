" --- General Configuration ---
set tabstop=4
"set noexpandtab
set showcmd

" --- vim-plug configuration ---
call plug#begin('~/.vim/plugs')
" UltiSnips - snippet manager
Plug 'SirVer/ultisnips'

let g:UltiSnipsExpandTrigger='<tab>'
let g:UltiSnipsJumpForwardTrigger='<tab>'
let g:UltiSnipsJumpBackwardTrigger='<s-tab>'
let g:UltiSnipsEditSplit='tabdo'

" vimtex - 
"Plug 'lervag/vimtex'
"let g:tex_flavor='latex'
"let g:vimtex_view_method='zathura'
"let g:vimtex_quickfix_mode=0
"set conceallevel=1
"let g:tex_conceal='abdmg'

" surround.vim - for surrounding text
Plug 'tpope/vim-surround'

" airline - status/tabline
Plug 'vim-airline/vim-airline'
let g:airline#extensions#tabline#enabled = 1

Plug 'vim-airline/vim-airline-themes'
let g:airline_theme='bubblegum'

Plug 'ParamagicDev/vim-medic_chalk'
Plug 'pablopunk/sick.vim'

call plug#end()

colorscheme medic_chalk
