local lspconfig = require('lspconfig')

lspconfig.ruff.setup({
  on_attach = function(client, bufnr)
    vim.api.nvim_create_autocmd("BufWritePre", {
      buffer = bufnr,
      callback = function()
        vim.lsp.buf.format({ bufnr = bufnr })
      end,
    })
  end,
  init_options = {
    settings = {
      ruff = {
        formatOnSave = true,
      }
    }
  }
})

lspconfig.pyright.setup({
  settings = {
    pyright = {
      -- Using Ruff's import organizer	
      disableOrganizeImports = true,
    },
    python = {
      typeCheckingMode = 'strict',
      diagnosticSource = 'mypy',
      analysis = {
        -- Ignore all files for analysis to exclusively use Ruff for linting
        ignore = { "*" },
	useLibraryCodeForTypes = true,
	autoSearchPaths = true,
	diagnosticMode = "openFilesOnly",
      },
    },
  },
})

