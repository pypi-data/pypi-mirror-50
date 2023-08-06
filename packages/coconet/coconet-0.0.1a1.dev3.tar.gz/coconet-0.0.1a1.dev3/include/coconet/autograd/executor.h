#ifndef COCONET_AUTOGRAD_EXECUTOR_H_
#define COCONET_AUTOGRAD_EXECUTOR_H_

#include <memory>
#include <vector>

#include <coconet/autograd/variable.h>
#include <coconet/autograd/function.h>

namespace coconet
{
    namespace autograd
    {
        class Edge
        {
        public:
            std::vector<std::weak_ptr<IVariable>> input_list;
            std::weak_ptr<IVariable> output;
            std::shared_ptr<FunctionBase> fn;
		public:
			Edge(std::vector<std::weak_ptr<IVariable>> i, std::weak_ptr<IVariable> o, std::shared_ptr<FunctionBase> f)
				:input_list(i), output(o), fn(f)
			{

			}
        };

        class Node
        {
        private:
            std::shared_ptr<IVariable> variable;
		public:
			Node()
			{
			}

			Node(std::shared_ptr<IVariable> v)
				: variable(v)
			{
			}
        };

        class VariableGraph
        {
        private:
            std::vector<Edge> edge_list;
            std::vector<Node> node_list;
		public:
			void add_variable(std::shared_ptr<IVariable> v)
			{
				node_list.push_back(Node(v));
			}

			void add_edge(std::vector<std::weak_ptr<IVariable>> input_list, std::weak_ptr<IVariable> output, std::shared_ptr<FunctionBase> fn)
			{
				edge_list.push_back(Edge(input_list, output, fn));
			}
        };

        class Executor
        {

        };
    }
}


#endif //! COCONET_AUTOGRAD_EXECUTOR_H_