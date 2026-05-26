const MESSAGE = "Avoid direct .message on catch-bound errors. Use getErrorMessage() from src/lib/errors.js — the caught value may not be an Error instance.";
const DESTRUCTURED_MESSAGE = "Avoid destructuring .message from caught values. Use getErrorMessage() from src/lib/errors.js — the caught value may not be an Error instance.";

function findVariable(scope, name) {
  let s = scope;

  while (s) {
    const v = s.variables.find((variable) => variable.name === name);

    if (v) {
      return v;
    }

    s = s.upper;
  }

  return null;
}

function isMessageProperty(node) {
  if (node.computed) {
    return node.property.type === "Literal" && node.property.value === "message";
  }

  return node.property.type === "Identifier" && node.property.name === "message";
}

function getVariable(node, sourceCode) {
  if (!node || node.type !== "Identifier") {
    return null;
  }

  const scope = sourceCode.getScope(node);

  return findVariable(scope, node.name);
}

function getMessagePropertyBinding(node) {
  let current = node;

  while (current.parent?.type === "AssignmentPattern") {
    current = current.parent;
  }

  const parent = current.parent;

  if (parent?.type !== "Property") {
    return null;
  }

  if (!parent.computed) {
    return parent.key.type === "Identifier" && parent.key.name === "message"
      ? parent
      : null;
  }

  return parent.key.type === "Literal" && parent.key.value === "message"
    ? parent
    : null;
}

function isCatchObjectVariable(variable, sourceCode, seen = new Set()) {
  if (!variable || seen.has(variable)) {
    return false;
  }

  seen.add(variable);

  return variable.defs.some((def) => {
    if (def.type === "CatchClause") {
      return def.name?.type === "Identifier" && def.name.parent?.type === "CatchClause";
    }

    if (def.type !== "Variable" || def.node.type !== "VariableDeclarator") {
      return false;
    }

    return def.name?.type === "Identifier"
      && def.node.id === def.name
      && isCatchObjectVariable(getVariable(def.node.init, sourceCode), sourceCode, seen);
  });
}

function isCatchMessageVariable(variable, sourceCode, seen = new Set()) {
  if (!variable || seen.has(variable)) {
    return false;
  }

  seen.add(variable);

  return variable.defs.some((def) => {
    if (def.type === "CatchClause") {
      return def.node.param?.type === "ObjectPattern" && Boolean(getMessagePropertyBinding(def.name));
    }

    if (def.type !== "Variable" || def.node.type !== "VariableDeclarator") {
      return false;
    }

    if (def.name?.type === "Identifier" && def.node.id === def.name) {
      return isCatchMessageVariable(getVariable(def.node.init, sourceCode), sourceCode, seen);
    }

    return def.node.id.type === "ObjectPattern"
      && Boolean(getMessagePropertyBinding(def.name))
      && isCatchObjectVariable(getVariable(def.node.init, sourceCode), sourceCode, seen);
  });
}

function isCatchBoundIdentifier(node, sourceCode) {
  return isCatchObjectVariable(getVariable(node.object, sourceCode), sourceCode);
}

function isReadReference(node, sourceCode) {
  const variable = getVariable(node, sourceCode);

  return variable?.references.some((reference) => reference.identifier === node && reference.isRead()) ?? false;
}

export default {
  meta: {
    type: "problem",
    docs: {
      description: "Disallow accessing .message on catch-bound error variables",
      recommended: false,
    },
    schema: [],
    messages: {
      avoidCatchMessage: MESSAGE,
      avoidCatchDestructuredMessage: DESTRUCTURED_MESSAGE,
    },
  },
  create(context) {
    const sourceCode = context.sourceCode;

    function reportIfCatchMessage(node) {
      if (!isMessageProperty(node)) {
        return;
      }

      if (!isCatchBoundIdentifier(node, sourceCode)) {
        return;
      }

      context.report({
        node,
        messageId: "avoidCatchMessage",
      });
    }

    function reportIfCatchDestructuredMessage(node) {
      if (!isReadReference(node, sourceCode)) {
        return;
      }

      if (!isCatchMessageVariable(getVariable(node, sourceCode), sourceCode)) {
        return;
      }

      context.report({
        node,
        messageId: "avoidCatchDestructuredMessage",
      });
    }

    return {
      Identifier: reportIfCatchDestructuredMessage,
      "MemberExpression[property.name='message']": reportIfCatchMessage,
      "MemberExpression[computed=true][property.type='Literal'][property.value='message']": reportIfCatchMessage,
    };
  },
};
