" Quickly edit/reload this configuration file
nnoremap gev :tabe $MYVIMRC<CR>
nnoremap gsv :so $MYVIMRC<CR>

syntax on                       " Syntax highlighting
set background=dark             " Terminal with a dark background
set t_Co=256
set expandtab                   " Make a tab to spaces, num of spaces set in tabstop
set shiftwidth=4                " Number of spaces to use for autoindenting
set tabstop=4                   " A tab is four spaces
set smarttab                    " insert tabs at the start of a line according to
set list                        " show invisible characters
set listchars=tab:>·,trail:·    " but only show tabs and trailing whitespace
set number                      " Enable line numbers
set numberwidth=3               " Line number width
highlight LineNr term=bold cterm=NONE ctermfg=DarkGrey ctermbg=NONE gui=NONE guifg=DarkGrey guibg=NONE
set complete-=.,w,u,t,i
set mouse=a
set backspace=indent,eol,start

let g:vdebug_options = {}
let g:vdebug_options["socket_type"] = 'unix'
let g:vdebug_options["unix_path"] = '/var/run/dbgp/uwsgi.sock'
let g:vdebug_options["unix_permissions"] = 0777
let g:vdebug_options["break_on_open"] = 0
let g:vdebug_options["continuous_mode"] = 1

" This can be 'compact' or 'expanded'.
let g:vdebug_options["watch_window_style"] = 'expanded'

let g:vdebug_features = {}
let g:vdebug_features['max_children'] = 512
let g:vdebug_features['max_data'] = 1000000

" CtrlP settings
let g:ctrlp_max_files = 0
let g:ctrlp_clear_cache_on_exit=0
let g:ctrlp_cache_dir = $HOME . '/.cache/ctrlp'
if executable('ag')
    let g:ctrlp_user_command = 'ag %s -l --nocolor -g ""'
endif

" Load vim-plug
if empty(glob("~/.vim/autoload/plug.vim"))
    execute '!curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
endif

call plug#begin('~/.vim/plugged')
Plug 'Yggdroot/indentLine'
Plug 'vim-airline/vim-airline'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'JazzCore/ctrlp-cmatcher'
Plug 'powerline/powerline'
call plug#end()
