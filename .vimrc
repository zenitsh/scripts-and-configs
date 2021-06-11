set tabstop=4
set shiftwidth=4
set number
set autoindent
set splitright
set splitbelow

call plug#begin('~/.vim/plugged')
Plug 'itchyny/lightline.vim'
Plug 'Shougo/deoplete.nvim'
Plug 'Shougo/neosnippet'
Plug 'Shougo/neosnippet-snippets'
Plug 'Shougo/deoplete-clangx'
Plug 'roxma/nvim-yarp'
Plug 'roxma/vim-hug-neovim-rpc'
Plug 'tomasr/molokai'
Plug 'scrooloose/nerdtree'
Plug 'vim-scripts/taglist.vim'
call plug#end()

let g:deoplete#enable_at_startup=1
colorscheme molokai

nmap <leader>k :hi Normal ctermfg=252 ctermbg=none<CR>
nmap <leader>l :hi Normal ctermfg=252 ctermbg=0<CR>
nmap <leader>000 <C-c>:qa!
nmap <leader>z; <C-c>:!
nmap <leader>zz; <C-c>:cd<Space>
hi Normal ctermfg=252 ctermbg=0
set completeopt=menu

nmap <leader>[ :NERDTreeToggle<CR>:TlistToggle<CR>
nmap <leader>w 33<C-w>l
nmap <leader>q 33<C-w>h
nmap <leader>] <C-w>w
nmap <leader>oo; t:TlistToggle<CR>
nmap <leader>o; t:NERDTreeToggle<CR>:TlistToggle<CR>
nmap <F5> :!gcc % -o %.out<CR>
nmap <F9> :ter ./%.out<CR>
nmap <F10> :!gcc -g % -o %.out<CR>:ter gdb %.out<CR>
nmap <F11> :!gcc % -o %.out<CR>:ter ./%.out<CR>



func SetAuthor(prefix)
	call setline(1,a:prefix)
	call append(line("."),a:prefix."\tCreated by Zhang Wenhan at ".localtime()."s after 1970.1.1 00:00")
	call append(line(".")+1,a:prefix."\thttps://zwhsh.github.io")
	call append(line(".")+2,a:prefix)
endfunc

func SetContent(type)
	if a:type=="c"
		call append(line(".")+3,"#include <stdio.h>")
		call append(line(".")+4,"#include <stdlib.h>")
		call append(line(".")+5,"")
		call append(line(".")+6,"int main(int argn,char **argv)")
		call append(line(".")+7,"{")
		call append(line(".")+8,"")
		call append(line(".")+9,"	return 0;")
		call append(line(".")+10,"}")
	endif
endfunc

autocmd BufNewFile *.c exec SetAuthor("//") && exec SetContent("c") 
autocmd BufWritePost *.c echo "<F5> Compile <F9> Run <F10> Debug <F11> Compile & Run" 

let NERDTreeChDirMode=2

let Tlist_Ctags_Cmd='/usr/bin/ctags'
let Tlist_Show_One_File=1
let Tlist_Exit_OnlyWindow=1
let Tlist_Use_Right_Window=1

func Init()
	if expand("%")==""
		cd CodeBase
		NERDTreeToggle
		echo "Input \":cd <Your Project>\""
	endif
endfunc

