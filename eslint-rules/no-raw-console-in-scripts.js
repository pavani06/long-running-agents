/**
 * Canonical helper names exported by src/lib/safe-console.js.
 *
 * Used to validate:
 * - Named imports: only these identifiers are trusted from safe-console.js
 * - Namespace member access: `safe.safeText(...)` is safe, `safe.unknown(...)` is not
 *
 * When safe-console.js gains a new export, add it here.
 */
const KNOWN_HELPERS = new Set([
  'safeError',
  'safeValidationError',
  'safePhone',
  'safeConversationId',
  'safeBaseUrl',
  'safeToken',
  'safeText',
  'safeSideEffects',
  'safeResponse',
]);

/**
 * Match import paths that resolve to the canonical safe-console module.
 * Requires a path separator (or start-of-string) before `safe-console.js`
 * to prevent false matches like `my-safe-console.js`.
 */
const SAFE_CONSOLE_PATH = /(^|[/\\])safe-console\.js$/;

export default {
  meta: {
    type: 'suggestion',
    docs: {
      description:
        'Disallow raw console.log/warn/error calls in scripts; use safe-console helpers instead',
      recommended: false,
    },
    schema: [],
    messages: {
      noRawConsole:
        'Avoid raw console.log/warn/error calls. Use safe-console helpers (safeText, safeError, etc.) from src/lib/safe-console.js',
    },
  },
  create(context) {
    const safeBindings = new Set();
    const namespaceBindings = new Set();

    const isSafeArgument = (node) => {
      if (node.type === 'CallExpression') {
        if (
          node.callee.type === 'Identifier' &&
          safeBindings.has(node.callee.name)
        ) {
          return true;
        }

        if (
          node.callee.type === 'MemberExpression' &&
          !node.callee.computed &&
          node.callee.object.type === 'Identifier' &&
          namespaceBindings.has(node.callee.object.name) &&
          node.callee.property.type === 'Identifier' &&
          KNOWN_HELPERS.has(node.callee.property.name)
        ) {
          return true;
        }
      }

      if (node.type === 'TemplateLiteral') {
        return (
          node.expressions.length > 0 &&
          node.expressions.every((expr) => isSafeArgument(expr))
        );
      }

      return false;
    };

    return {
      ImportDeclaration(node) {
        if (!SAFE_CONSOLE_PATH.test(node.source.value)) {
          return;
        }

        for (const spec of node.specifiers) {
          if (
            spec.type === 'ImportSpecifier' &&
            KNOWN_HELPERS.has(spec.imported.name)
          ) {
            safeBindings.add(spec.local.name);
            continue;
          }

          if (
            spec.type === 'ImportNamespaceSpecifier' ||
            spec.type === 'ImportDefaultSpecifier'
          ) {
            namespaceBindings.add(spec.local.name);
          }
        }
      },
      'CallExpression[callee.type="MemberExpression"][callee.object.name="console"]'(
        node
      ) {
        // Skip computed access like console['log'] — not statically analyzable
        if (node.callee.computed) return;

        const method = node.callee.property.name;
        if (!['log', 'warn', 'error'].includes(method)) {
          return;
        }

        // Flag bare console.log() with no arguments
        if (node.arguments.length === 0) {
          context.report({
            node,
            messageId: 'noRawConsole',
          });
          return;
        }

        // Check if all arguments are safe
        const allArgumentsSafe = node.arguments.every(isSafeArgument);

        if (!allArgumentsSafe) {
          context.report({
            node,
            messageId: 'noRawConsole',
          });
        }
      },
    };
  },
};
