# -*- coding: utf-8 -*-

from blockstate import ExpressionState
from optimizer import Optimizer
from expressionblock import ExpressionBlock
from expressions import *
from instructions import *
from opcodes import special_ops
import sys
import logging

def get_single_usage(begin, expressions, live):
	"""
	得到单次用法
	:param begin:
	:param expressions:
	:param live:
	:return:
	"""
	target_expression = expressions[begin]
	write = target_expression.get_write_registers().pop()

	index, count = -1, 0
	overwritten = False
	for i, expression in enumerate(expressions):
		if i < begin + 1:
			continue

		if write in expression.get_read_registers():
			count += 1
			index = i
		if expression.writes_to(write):
			overwritten = True
			break
	if not overwritten and write in live:
		return -1

	if count == 1:
		return index
	return -1


def is_valid_at(expressions, begin, end):
	"""
	表达式是否有效
	:param expressions:
	:param begin:
	:param end:
	:return:
	"""
	target_expression = expressions[begin]
	for expression in expressions[begin + 1:end]:
		if expression.invalidates(target_expression):
			return False
	return True


class Aggregator(Optimizer):
	"""聚合"""
	def __init__(self, binary):
		logging.info("聚合器初始化")
		Optimizer.__init__(self, binary)  # 初始化优化器
		for func in self.get_all_functions():
			self.__convert_function(func)

	def __convert_function(self, func):
		"""
		转换函数
		:param func:
		:return:
		"""
		logging.info("聚合器：转换函数：" + '{:#x}'.format(func.signature))
		for block in func.graph:
			new_block = ExpressionBlock(block.get_id(), block.get_entry_address())
			new_block.exit_stack_size = block.exit_stack_size
			for instruction in block:
				expression = self.__convert_instruction(instruction)
				if expression:
					new_block.append_expression(expression)
			func.graph.replace_block(new_block)
		# return

		outs = self.get_liveness_states(func)
		for block in func.graph:
			block_id = block.get_id()
			# if block_id != 41:
			# 	continue

			live = outs[block_id]
			change, count = True, 0
			while change:
				# self.__aggregate_expressions(block)
				self.__aggregate_single(block, live)
				change = self.__eliminate_dead_expression(block, live)
				count += 1
			# if block_id == 95:
			# 	block.debug_block()
			# 	print(live)

	@staticmethod
	def __convert_instruction(instruction):
		"""
		转换指令
		:param instruction: 指令
		:return:
		"""
		opcode = instruction.opcode
		reads = instruction.reads
		writes = instruction.writes
		address = instruction.address

		if opcode == "MOVE":
			return MoveExpression(opcode, reads, writes, address)
		elif isinstance(instruction, BinOpInstruction):
			return BinOpExpression(opcode, reads, writes, address)
		elif isinstance(instruction, MonoOpInstruction):
			return MonoOpExpression(opcode, reads, writes, address)
		elif opcode == "JUMP":
			return JumpExpression(opcode, reads, writes, address)
		elif opcode == "JUMPI":
			return JumpIExpression(opcode, reads, writes, address)
		elif isinstance(instruction, MstoreInstruction):
			return MstoreExpression(opcode, reads, writes, address)
		elif isinstance(instruction, MloadInstruction):
			return MloadExpression(opcode, reads, writes, address)
		elif isinstance(instruction, CallLoadInstruction):
			return CallLoadExpression(opcode, reads, writes, address)
		elif isinstance(instruction, IntCallInstruction):
			return IntCallExpression(opcode, reads, writes, address)
		elif isinstance(instruction, SstoreInstruction):
			return SstoreExpression(opcode, reads, writes, address)
		elif isinstance(instruction, SloadInstruction):
			return SloadExpression(opcode, reads, writes, address)
		elif opcode in special_ops:
			return SpecialExpression(opcode, reads, writes, address)
		elif opcode in fake_ops:
			return FakeExpression(opcode, reads, writes, address)
		elif opcode not in {"NOP"}:
			return Expression(opcode, reads, writes, address)

	@staticmethod
	def __aggregate_expressions(block):
		"""
		聚合表达式
		:param block:
		:return:
		"""
		table = ExpressionState()
		for expression in block:
			table.apply_mapping(expression)
			table.add_mapping(expression)

	@staticmethod
	def __aggregate_single(block, live):
		"""
		聚合单个？
		:param block:
		:param live:
		:return:
		"""
		expressions = block.get_items()

		for i, expression in enumerate(expressions):
			writes = expression.get_write_registers()
			opcode = expression.opcode
			if "INTCALL" in opcode or \
				len(writes) != 1:
				continue

			j = get_single_usage(i, expressions, live)
			if j == -1:
				continue

			if is_valid_at(expressions, i, j):
				target = expression.writes[0]
				count = expressions[j].get_read_count(target)
				if count == 1:
					expressions[j].set_dependency(target, expression)
					block.set_pass_expression(i)

		# block.debug_block()
		# sys.exit()

	@staticmethod
	def __eliminate_dead_expression(block, out):
		"""
		消除死亡表达？
		:param block:
		:param out:
		:return:
		"""
		change = False

		new_expressions = list()
		expressions = block.get_items()
		for expression in reversed(expressions):
			writes = expression.get_write_registers()
			reads = expression.get_read_registers()
			opcode = expression.opcode
			if len(writes & out) == 0 and\
				opcode in throw_away_ops | {"SLOAD"}:
				change = True
				continue
			else:
				out = (out - writes) | reads
				new_expressions.append(expression)
		new_expressions.reverse()
		block.set_items(new_expressions)
		return change
		# block.debug_block()

	def visualize_functions(self, step):
		"""
		可视化功能
		:return:
		"""
		for func in self.get_all_functions():
			func.visualize_function(step)


if __name__ == "__main__":
	input_file = open(sys.argv[1])
	line = input_file.readline().strip()
	if " " in line:
		line = line.split(" ")[1]
	input_file.close()
	a = Aggregator(line)
	if "-d" in sys.argv:
		a.debug_functions()
	if "-v" in sys.argv:
		a.visualize_functions("4.Aggregator.")
