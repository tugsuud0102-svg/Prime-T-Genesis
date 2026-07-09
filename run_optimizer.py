from core.optimizer import run_optimizer


if __name__ == "__main__":
    top_results = run_optimizer()
    print("TOP OPTIMIZER RESULTS")
    for result in top_results:
        print(result)
