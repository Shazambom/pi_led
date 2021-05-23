import copy

class Sorter:
	def __init__(self, report):
		self.report = report

	def swap(self, l, i, j):
		l[i], l[j] = l[j], l[i]
		self.report(copy.deepcopy(l))

	def merge_sort(self, lst, left, right):
		if left < right:
			center = int((left + right - 1) / 2)
			self.merge_sort(lst, left, center)
			self.merge_sort(lst, center + 1, right)
			self.merge(lst, left, center, right)

	def merge(self, lst, start, mid, end):
		start2 = mid + 1
		if (lst[mid] <= lst[start2]):
			return
		
		while start <= mid and start2 <= end:
			if lst[start] <= lst[start2]:
				start += 1
			else:
				lst.insert(start, lst.pop(start2))
				start += 1
				mid += 1
				start2 += 1
			self.report(copy.deepcopy(lst))


	def quick_sort(self, lst, left, right):
		if left < right:
			p = self.partition(lst, left, right)
			self.quick_sort(lst, left, p)
			self.quick_sort(lst, p + 1, right)

	def partition(self, lst, left, right):
		pivot, ind = self.pick_pivot(lst, left, right)
		self.swap(lst, ind, right-1)
		i = left
		for j in range(left, right):
			if lst[j] < pivot:
				self.swap(lst, i, j)
				i += 1
		self.swap(lst, i, right-1)
		return i

	def pick_pivot(self, lst, left, right):
		center = left + int((right - left) / 2)
		avg = (lst[center] + lst[left] + lst[right-1]) / 3
		left_delta = abs(avg - lst[left])
		right_delta = abs(avg - lst[right-1])
		center_delta = abs(avg - lst[center])
		if left_delta < right_delta and left_delta < center_delta:
			return lst[left], left
		elif right_delta < center_delta:
			return lst[right-1], right-1
		else:
			return lst[center], center

	def comb_sort(self, arr):
		gap = len(arr)
		shrink = 1.3
		is_sorted = False
		while not is_sorted:
			gap = int(gap/shrink)
			if gap <= 1:
				gap = 1
				is_sorted = True
			for i in range(0, len(arr) - gap):
				if arr[i] > arr[i + gap]:
					self.swap(arr, i, i + gap)
					is_sorted = False



# import time
# import random



# frame_list = []
# sorter = Sorter(lambda l: frame_list.append(l))
# lst = random.sample(range(10), 10)

# merge_lst = copy.deepcopy(lst)
# quick_lst = copy.deepcopy(lst)
# comb_lst = copy.deepcopy(lst)

# merge_time = time.process_time()
# sorter.merge_sort(merge_lst, 0, len(merge_lst) - 1)
# print(time.process_time() - merge_time)
# print("Is sorted? " + str(sorted(merge_lst) == merge_lst))
# print(frame_list)

# frame_list = []
# quick_time = time.process_time()
# sorter.quick_sort(quick_lst, 0, len(quick_lst))
# print(time.process_time() - quick_time)
# print("Is sorted? " + str(sorted(quick_lst) == quick_lst))
# print(frame_list)

# frame_list = []
# comb_time = time.process_time()
# sorter.comb_sort(comb_lst)
# print(time.process_time() - comb_time)
# print("Is sorted? " + str(sorted(comb_lst) == comb_lst))
# print(frame_list)



